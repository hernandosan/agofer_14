# -*- coding: utf-8 -*-

from odoo import models, fields, api


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

    @api.depends_context('force_company')
    def _compute_credit_maturity(self):
        tables, where_clause, where_params = self.env['account.move.line'].with_context(state='posted', company_id=self.env.company.id, aged_balance=True, date_to=fields.Date.today())._query_get()
        where_params = [tuple(self.ids)] + where_params
        if where_clause:
            where_clause = 'AND ' + where_clause
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
        for pid, type, val in self._cr.fetchall():
            partner = self.browse(pid)
            if type == 'receivable':
                partner.credit_maturity = val
                if partner not in treated:
                    treated |= partner
        remaining = (self - treated)
        remaining.credit_maturity = False

    @api.depends('credit_limit', 'credit_maturity')
    def _compute_credit_quota(self):
        for partner in self:
            partner.credit_quota = partner.credit_limit - partner.credit
