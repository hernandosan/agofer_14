# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AccountConsignment(models.Model):
    _name = 'account.consignment'
    _description = 'Account Consignment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    amount = fields.Monetary('Amount', tracking=True)
    amount_invoice = fields.Monetary('Amount Invoice', compute='_compute_amount_invoice')
    bank_id = fields.Many2one('res.bank', 'Bank', tracking=True)
    # branch = fields.Char('Branch')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company, readonly=True)
    consignment_bool = fields.Boolean('Reconcile', default=True, copy=False, help='Reconcile difference')
    currency_id = fields.Many2one(related='company_id.currency_id', readonly=True)
    date = fields.Date('Date', default=fields.Date.today())
    date_consignment = fields.Date('Date consignment', default=fields.Date.today())
    invoices_ids = fields.Many2many('account.move', string='Invoices', copy=False)
    journal_id = fields.Many2one(related='bank_id.journal_id')
    move_id = fields.Many2one('account.move', 'Account move', readonly=True, copy=False)
    name = fields.Char('Number', required=True, readonly=True, default=_('New'))
    order_id = fields.Many2one('sale.order', 'Sale order')
    partner_id = fields.Many2one('res.partner', 'Partner', tracking=True)
    reference = fields.Char('Reference', tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Cancel')], 'State', 
        required=True, default='draft', copy=False, tracking=True)
    team_id = fields.Many2one('crm.team', 'CRM Team')
    type = fields.Selection([('normal','Payment'),('advance','Advance'),('crossover','Crossover')], 'Type consignment', 
        copy=False, default='normal')
    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user, readonly=True)

    @api.depends('invoices_ids')
    def _compute_amount_invoice(self):
        for consignment in self:
            if consignment.invoices_ids:
                consignment.amount_invoice = sum(invoice.currency_id.with_context(date=invoice.invoice_date).compute(invoice.amount_residual, self.currency_id) for invoice in self.invoices_ids) or 0.0
            else:
                consignment.amount_invoice = 0.0

    @api.model
    def create(self, vals):
        vals.update(name=self.env['ir.sequence'].next_by_code('account.consignment') or _('New'))
        return super(AccountConsignment, self).create(vals)

    def action_confirm(self):
        for consignment in self:
            consignment._action_confirm()
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_draft(self):
        self.write({'state': 'draft'})

    def _action_confirm(self):
        self.ensure_one()
        move_id = self._action_payment()
        self.write({'move_id': move_id})

    def _action_payment(self):
        self.ensure_one()
        vals = self._prepare_move_vals()
        payment_id = self.env['account.payment'].create(vals)
        payment_id.action_post()
        move_id = payment_id.move_id
        self._action_crossover(move_id)
        return move_id

    def _action_crossover(self, move_id):
        self.ensure_one()
        if self.type != 'crossover' or not self.invoices_ids:
            return False
        id = move_id.line_ids.filtered(lambda l: l.account_id.user_type_id.type == 'receivable')
        ids = self.invoices_ids.line_ids.filtered(lambda l: l.account_id.user_type_id.type == 'receivable')
        lines = id + ids
        lines.reconcile()
        return True

    def _prepare_move_vals(self):
        journal_id = self.journal_id
        partner_id = self.partner_id
        team_id = self.team_id
        if not journal_id:
            raise ValidationError(_("The Bank %s has not journal") % self.bank_id.id)
        if self.type == 'crossover' and self.invoices_ids:
            account_id = self.invoices_ids.line_ids.filtered(lambda l: l.account_id.user_type_id.type == 'receivable').account_id
            if len(account_id) > 1:
                raise ValidationError(_("The invoices have different accounts receivable. \n Create a payment and reconcile"))
        else:
            account_id = team_id._team_advance_account()
        vals = {
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'partner_id': partner_id.id,
            'destination_account_id': account_id.id,
            'amount': self.amount,
            'currency_id': self.currency_id.id,
            'date': self.date_consignment,
            'journal_id': journal_id.id,
            'order_id': self.order_id.id if self.order_id else False,
            'ref': _('Consignment %s') % self.name,
        }
        if self.type == 'crossover' and self.amount_invoice != self.amount and self.consignment_bool:
            amount_consignment = self.amount
            amount_invoice = self.amount_invoice
            amount = amount_consignment - amount_invoice
            account_id = journal_id.payment_income_account_id if amount > 0 else journal_id.payment_expense_account_id
            write_off_line_vals = {
                'name': _('Reconcile Consignment %s') % self.name,
                'amount': amount if amount > 0 else -amount,
                'account_id': account_id.id,
            }
            vals.update(write_off_line_vals=write_off_line_vals)
        return vals
