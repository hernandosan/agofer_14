# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    workcenter_costs_hour = fields.Float(related='workcenter_id.costs_hour', string='Cost per hour')
    duration_real = fields.Float('Real Duration', digits=(16, 2), help="Real duration (in minutes)")

    def button_finish(self):
        res = super(MrpWorkorder, self).button_finish()
        self.create_account_move()
        return res
    
    def create_account_move(self):
        for record in self:
            date = fields.Date.today()
            journal_id = self.env.ref('mrp_extended.journal_production')
            ref = record.production_id and record.production_id.name or ''
            ref += ' - '
            ref += record.name or ''
            line_ids = record._prepare_line_ids()
            val = {
                # 'currency_id': currency_id,
                'date': date,
                'journal_id': journal_id.id,
                'ref': ref,
                'type': 'entry',
                'line_ids': line_ids,
            }
            self.env['account.move'].sudo().create(val).action_post()
    
    def _prepare_line_ids(self):
        self.ensure_one()
        time_lines = self.time_ids.filtered(lambda x: x.date_end and not x.cost_already_recorded)
        duration = sum(time_lines.mapped('duration'))
        cost = (duration / 60.0) * self.workcenter_id.costs_hour_workcenter
        lines = []
        account_debit, account_credit = self._prepare_account_account()
        partner_id = self.env.user.company_id.partner_id
        name = self.production_id and self.production_id.name or ''
        name += ' - '
        name += self.workcenter_id and self.workcenter_id.name or ''
        # Debit
        val = {
            'account_id': account_debit,
            'partner_id': partner_id.id,
            'name': name,
            'debit': cost,
            'credit': 0.00,
        }
        lines.append((0,0,val))
        # Credit
        val = {
            'account_id': account_credit,
            'partner_id': partner_id.id,
            'name': name,
            'debit': 0.00,
            'credit': cost,
        }
        lines.append((0,0,val))
        for indirect in self.workcenter_id.line_ids:
            name = self.production_id and self.production_id.name or ''
            name += ' - '
            name += indirect.product_id.name
            debit_credit = indirect.costs_hour
            account_credit = indirect.account_id.id
            # Debit
            val = {
                'account_id': account_debit,
                'partner_id': partner_id.id,
                'name': name,
                'debit': debit_credit,
                'credit': 0.00,
            }
            lines.append((0,0,val))
            # Credit
            val = {
                'account_id': account_credit,
                'partner_id': partner_id.id,
                'name': name,
                'debit': 0.00,
                'credit': debit_credit,
            }
            lines.append((0,0,val))
        return lines

    def _prepare_account_account(self):
        self.ensure_one()
        credit = self.workcenter_id.account_id and self.workcenter_id or False
        if not credit:
            raise ValidationError(_("Account has not been set up in work center: %s") % self.workcenter_id.name)
        location_id = self.env['stock.location'].search([('usage','=','production')], order='id asc', limit=1)
        debit = location_id and location_id.valuation_out_account_id or False
        if not debit:
            production_id = self.production_id
            product_id = production_id.product_id
            categ_id = product_id.categ_id
            debit = categ_id.property_stock_valuation_account_id
            if not debit:
                raise ValidationError(_("Account has not been set up in product: %s") % product_id.name)
        return debit.id, credit.id