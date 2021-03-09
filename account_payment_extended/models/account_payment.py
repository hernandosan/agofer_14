# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    account_type = fields.Selection([('payment', 'Payment'), ('advance', 'Advance'), ('cross', 'Cross')], default='payment', required=True)
    amount_lines = fields.Monetary('Amount Lines', currency_field='currency_id', compute='_compute_amount_lines')
    branch_id = fields.Many2one('hr.branch', 'Branch')
    line_debit_ids = fields.One2many('payment.line', 'payment_debit_id','Debit lines')
    line_credit_ids = fields.One2many('payment.line', 'payment_credit_id','Credit lines')
    line_reconcile_id = fields.One2many('payment.line', 'payment_id', 'Lines')

    @api.onchange('branch_id')
    def _onchange_branch_id(self):
        if self.branch_id:
            if self.payment_type == 'inbound' and self.account_type == 'advance':
                journal_id = self.branch_id._account_advance().get('journal_customer_id')
                destination_account_id = self.branch_id._account_advance().get('account_customer_id')
            elif self.payment_type == 'outbound' and self.account_type == 'advance':
                journal_id = self.branch_id._account_advance().get('journal_supplier_id')
                destination_account_id = self.branch_id._account_advance().get('account_supplier_id')
            else:
                journal_id = False
                destination_account_id = False
            vals = {
                'journal_id': journal_id,
                'destination_account_id': destination_account_id
            }
            self.write(vals)

    @api.depends('account_type', 'line_debit_ids.total_currency', 'line_credit_ids.total_currency')
    def _compute_amount_lines(self):
        payments = self.filtered(lambda p: p.account_type == 'payment')
        for payment in payments:
            lines = payment.line_debit_ids if payment.payment_type == 'inbound' else payment.line_credit_ids
            amount = sum(lines.mapped('total_currency'))
            payment.update({'amount_lines': amount})
        (self - payments).update({'amount_lines': 0.0})

    def compute_lines(self):
        for payment in self.filtered(lambda p: p.account_type != 'advance'):
            payment._compute_lines()

    def _compute_lines(self):
        self.ensure_one()
        if self.account_type == 'cross':
            self._compute_line_ids('debit')
            self._compute_line_ids('credit')
        else:
            if self.payment_type == 'inbound':
                self._compute_line_ids('debit')
            else:
                self._compute_line_ids('credit')

    def _compute_line_ids(self, line_type):
        self.ensure_one()
        getattr(self, 'line_%s_ids' % line_type).unlink()
        field = 'line_%s_ids' % line_type
        self.write({field: self._prepare_line_ids(line_type)})

    def _prepare_line_ids(self, line_type):
        self.ensure_one()
        domain = self._prepare_domain_line(line_type)
        lines = self.env['account.move.line'].sudo().search(domain)
        return self._prepare_payment_line(lines, line_type)

    def _prepare_domain_line(self, line_type):
        self.ensure_one()
        domain = [
            ('partner_id', '=', self.partner_id.id),
            ('account_id', '=', self.destination_account_id.id),
            ('amount_residual', '>', 0.0),
            ('reconciled', '!=', True),
        ]
        if line_type == 'debit':
            domain += [
                ('account_id.internal_type', '=', 'receivable'),
                ('debit', '>', 0.0)
            ]
        if line_type == 'credit':
            domain += [
                ('account_id.internal_type', '=', 'payable'),
                ('credit', '>', 0.0)
            ]
        return domain

    def _prepare_payment_line(self, lines, line_type):
        self.ensure_one()
        line_ids = []
        for line in lines:
            vals = {
                'payment_debit_id': self.id, 
                'line_id': line.id,
                'account_id': line.account_id.id,
                'amount': line.balance,
                'amount_currency': line.amount_currency,
                'amount_residual': line.amount_residual,
                'amount_residual_currency': line.amount_residual_currency,
                'currency_id': self.currency_id.id,
                'currency_company_id': self.company_currency_id.id,
                'date': line.date,
                'date_maturity': line.date_maturity,
                'date_payment': self.date,
                'total': 0.0
            }
            line_ids.append((0, 0, vals))
        return line_ids

    def action_post(self):
        for payment in self.filtered(lambda p: p.account_type == 'payment'):
            payment.write({'amount': payment.amount_lines})
        res = super(AccountPayment, self).action_post()
        for payment in self.filtered(lambda p: p.account_type == 'payment'):
            set1 = payment.move_id.line_ids.filtered(lambda l: l.account_id == payment.destination_account_id)
            lines = payment.line_debit_ids if payment.payment_type == 'inbound' else payment.line_credit_ids
            set2 = lines.line_id
        (set1 | set2).reconcile()
        return res
