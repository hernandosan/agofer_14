# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    def create_account_move_line(self):
        for workorder in self.filtered(lambda w: w.production_id):
            workorder._create_account_move_line()

    def _create_account_move_line(self):
        self.ensure_one()
        if not self.production_id:
            return False
        journal_id, acc_src, acc_dest, acc_valuation = self._get_account_data()
        AccountMove = self.env['account.move'].with_context(default_journal_id=journal_id)
        description = '%s - %s' % (self.production_id.name, self.workcenter_id.name)
        move_lines = self._prepare_account_move_line(acc_dest, acc_valuation, description)
        if not move_lines:
            return False
        if move_lines:
            date = self._context.get('force_period_date', fields.Date.context_today(self))
            new_account_move = AccountMove.sudo().create({
                'journal_id': journal_id,
                'line_ids': move_lines,
                'date': date,
                'ref': description,
                'move_type': 'entry',
            })
            new_account_move._post()

    def _get_account_data(self):
        self.ensure_one()
        self = self.with_company(self.company_id)
        location = self.production_id.product_id.with_company(self.company_id).property_stock_production

        accounts_data_production = self.production_id.product_id.product_tmpl_id.get_product_accounts()

        if location.valuation_out_account_id:
            acc_src = location.valuation_out_account_id.id
        else:
            acc_src = accounts_data_production['stock_input'].id

        if location.valuation_in_account_id:
            acc_dest = location.valuation_in_account_id.id
        else:
            acc_dest = accounts_data_production['stock_output'].id

        accounts_data_workorder = self.workcenter_id.product_id.product_tmpl_id.get_product_accounts()

        acc_valuation = accounts_data_workorder.get('expense').id

        journal_id = accounts_data_production.get('stock_journal').id

        return journal_id, acc_src, acc_dest, acc_valuation

    def _prepare_account_move_line(self, debit_account_id, credit_account_id, description):
        self.ensure_one()

        time_lines = self.time_ids.filtered(lambda x: x.date_end and x.cost_already_recorded)
        duration = sum(time_lines.mapped('duration'))
        work_center_cost = (duration / 60.0) * self.workcenter_id.costs_hour
        if not work_center_cost:
            return False
        qty = duration / 60.0
        partner_id = self.env.company.partner_id.id
        debit_value = self.company_id.currency_id.round(work_center_cost)
        credit_value = debit_value

        debit_line_vals = {
            'name': description,
            'product_id': self.workcenter_id.product_id.id,
            'quantity': qty,
            'product_uom_id': self.workcenter_id.product_id.uom_id.id,
            'ref': description,
            'partner_id': partner_id,
            'debit': debit_value if debit_value > 0 else 0,
            'credit': -debit_value if debit_value < 0 else 0,
            'account_id': debit_account_id,
        }

        credit_line_vals = {
            'name': description,
            'product_id': self.product_id.id,
            'quantity': qty,
            'product_uom_id': self.product_id.uom_id.id,
            'ref': description,
            'partner_id': partner_id,
            'credit': credit_value if credit_value > 0 else 0,
            'debit': -credit_value if credit_value < 0 else 0,
            'account_id': credit_account_id,
        }

        rslt = {'credit_line_vals': credit_line_vals, 'debit_line_vals': debit_line_vals}
        if credit_value != debit_value:
            # for supplier returns of product in average costing method, in anglo saxon mode
            diff_amount = debit_value - credit_value
            price_diff_account = self.product_id.property_account_creditor_price_difference

            if not price_diff_account:
                price_diff_account = self.product_id.categ_id.property_account_creditor_price_difference_categ
            if not price_diff_account:
                raise UserError(_('Configuration error. Please configure the price difference account on the product or its category to process this operation.'))

            rslt['price_diff_line_vals'] = {
                'name': self.name,
                'product_id': self.product_id.id,
                'quantity': qty,
                'product_uom_id': self.product_id.uom_id.id,
                'ref': description,
                'partner_id': partner_id,
                'credit': diff_amount > 0 and diff_amount or 0,
                'debit': diff_amount < 0 and -diff_amount or 0,
                'account_id': price_diff_account.id,
            }
        return [(0, 0, line_vals) for line_vals in rslt.values()]
