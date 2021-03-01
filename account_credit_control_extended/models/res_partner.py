# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_control = fields.Boolean('Credit Control', default=True, tracking=True)
    credit_limit = fields.Monetary('Credit Limit', tracking=True)
    credit_type = fields.Selection([
        ('insured', 'Insured Quota'),
        ('administrative', 'Administrative Quota'),
        ('committee', 'Committee Quota')], 'Quota Type', default='insured', tracking=True)
    credit_maturity = fields.Monetary(compute='_compute_credit_maturity', string='Total Receivable Maturity')
    credit_quota = fields.Monetary(compute='_compute_credit_quota', string='Total Quota')
    document_ids = fields.One2many('credit.document', 'partner_id', 'Documents')

    @api.depends_context('force_company')
    def _compute_credit_maturity(self):
        tables, where_clause, where_params = self.env['account.move.line'].with_context(state='posted', company_id=self.env.company.id, aged_balance=True, date_to=fields.Date.today())._query_get()
        where_params = [tuple(self.ids)] + where_params
        if where_clause:
            where_clause = 'AND ' + where_clause
        if self.ids:
            self._cr.execute("""SELECT account_move_line.partner_id, act.type, SUM(account_move_line.amount_residual)
                        FROM """ + tables + """
                        LEFT JOIN account_account a ON (account_move_line.account_id=a.id)
                        LEFT JOIN account_account_type act ON (a.user_type_id=act.id)
                        WHERE act.type IN ('receivable','payable')
                        AND account_move_line.partner_id IN %s
                        AND account_move_line.reconciled IS NOT TRUE
                        """ + where_clause + """
                        GROUP BY account_move_line.partner_id, act.type
                        """, where_params)
        treated = self.browse()
        if self.ids:
            for pid, type, val in self._cr.fetchall():
                partner = self.browse(pid)
                if type == 'receivable':
                    partner.credit_maturity = val
                    if partner not in treated:
                        treated |= partner
        remaining = (self - treated)
        remaining.credit_maturity = False

    @api.depends('credit_limit', 'credit')
    def _compute_credit_quota(self):
        for partner in self:
            partner.credit_quota = partner.credit_limit - partner.credit

    def action_credit_interest(self):
        action = self.env.ref('account_credit_control_extended.action_credit_interest_wizard').sudo()
        result = action.read()[0]
        ids = self._aml_maturity().ids
        result['context'] = {
            'default_partner_id': self.id,
            'default_lines_ids': [(6, 0, ids)],
        }
        return result

    def _aml_maturity(self):
        self.ensure_one()
        date = self._context.get('date_matirity') or fields.Date.today()
        domain = [
            ('partner_id', '=', self.id), 
            ('reconciled', '!=', True), 
            ('account_id.internal_type', '=', 'receivable'), 
            ('move_id.state', '=', 'posted'), 
            ('date_maturity', '<', date)
        ]
        return self.env['account.move.line'].search(domain)

    def credit_control_report(self):
        # Invoice
        invoice_lines = self._aml_maturity()
        invoice_total = sum(invoice_lines.move_id.mapped('amount_total_signed'))
        invoice_residual = sum(invoice_lines.move_id.mapped('amount_residual_signed'))
        # Sale Order
        sale_order = self.env['sale.order'].search([('partner_id', 'child_of', self.id), ('state', '=', 'draft')])
        sale_total = sum(sale_order.mapped('amount_total'))
        vals = {
            'date_today': fields.Date.today(),
            'body_lines': invoice_lines,
            'invoice_total': invoice_total,
            'invoice_residual': invoice_residual,
            'sale_order': sale_order,
            'sale_total': sale_total,
        }
        return vals

    def days_maturity(self, date_invoice, date_maturity):
        return (fields.Date.from_string(date_invoice) - fields.Date.from_string(date_maturity)).days
