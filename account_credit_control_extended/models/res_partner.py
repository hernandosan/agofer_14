# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_control = fields.Boolean('Credit Control')
    credit_limit = fields.Monetary('Credit Limit', tracking=True)
    credit_type = fields.Selection([
        ('insured','Insured Quota'),
        ('administrative','Administrative Quota'),
        ('committee','Committee Quota')], 'Quota Type', tracking=True)
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
        domain = [
            ('partner_id', '=', self.id), 
            ('full_reconcile_id', '=', False), 
            ('balance', '!=', 0), 
            ('account_id.reconcile', '=', True), 
            ('date_maturity', '<', fields.Date.today()), 
            ('move_id.move_type', '=', 'out_invoice')
        ]
        ids = self.env['account.move.line'].search(domain).ids
        result['context'] = {
            'default_partner_id': self.id,
            'default_lines_ids': [(6, 0, ids)],
        }
        return result
