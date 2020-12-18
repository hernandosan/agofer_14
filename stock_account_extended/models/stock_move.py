# -*- coding: utf-8 -*-

from collections import defaultdict

from odoo import api, fields, models, _
from odoo.tools import float_is_zero


class StockMove(models.Model):
    _inherit = 'stock.move'

    standard_price = fields.Float('Cost', digits='Product Price', copy=False)
    cost_id = fields.Many2one('stock.landed.cost', 'Landed Cost', copy=False)
    additional_cost = fields.Float('Additional Landed Cost', digits='Account', copy=False)

    @api.model
    def _get_valued_types(self):
        res = super(StockMove, self)._get_valued_types()
        res.append('int')
        return res

    def _get_int_move_lines(self):
        self.ensure_one()
        res = self.env['stock.move.line']
        for move_line in self.filtered(lambda m: m.cost_id).move_line_ids:
            if move_line.owner_id and move_line.owner_id != move_line.company_id.partner_id:
                continue
            if move_line.location_id._should_be_valued() and move_line.location_dest_id._should_be_valued():
                res |= move_line
        return res

    def _is_int(self):
        self.ensure_one()
        if self._get_int_move_lines():
            return True
        return False

    def _create_out_svl(self, forced_quantity=None):
        res = super(StockMove, self)._create_out_svl(forced_quantity=forced_quantity)
        for move in self:
            if move._is_out and move._is_returned('out'):
                res.filtered(lambda v: v.stock_move_id.id == move.id).write({
                    'value': self._get_price_unit() * res.quantity,
                    'unit_cost': self._get_price_unit(),
                })
        return res

    def _create_int_svl(self, forced_quantity=None):
        svl_vals_list = []
        for move in self:
            move = move.with_company(move.company_id)
            valued_move_lines = move._get_int_move_lines()
            valued_quantity = 0
            for valued_move_line in valued_move_lines:
                valued_quantity += valued_move_line.product_uom_id._compute_quantity(valued_move_line.qty_done, move.product_id.uom_id)
            unit_cost = abs(move.additional_cost)
            if move.product_id.cost_method == 'standard':
                unit_cost = move.product_id.standard_price
            svl_vals = move.product_id._prepare_int_svl_vals(forced_quantity or valued_quantity, unit_cost)
            svl_vals.update(move._prepare_common_svl_vals())
            if forced_quantity:
                svl_vals['description'] = 'Correction of %s (modification of past move)' % move.picking_id.name or move.name
            svl_vals_list.append(svl_vals)
        return self.env['stock.valuation.layer'].sudo().create(svl_vals_list)

    def _action_done(self, cancel_backorder=False):
        valued_moves = {valued_type: self.env['stock.move'] for valued_type in self._get_valued_types()}
        for move in self:
            if float_is_zero(move.quantity_done, precision_rounding=move.product_uom.rounding):
                continue
            for valued_type in self._get_valued_types():
                if getattr(move, '_is_%s' % valued_type)():
                    valued_moves[valued_type] |= move

        # AVCO application
        valued_moves['int'].product_price_update_before_done()
        valued_moves['out'].product_price_update_before_done()

        res = super(StockMove, self)._action_done(cancel_backorder=cancel_backorder)

        for move in self:
            move.write({'standard_price': move.product_id.standard_price})

        return res

    def product_price_update_before_done(self, forced_qty=None):
        res = super(StockMove, self).product_price_update_before_done(forced_qty=forced_qty)

        tmpl_dict = defaultdict(lambda: 0.0)
        std_price_update = {}
        for move in self.filtered(lambda move: ((move._is_out() and move._is_returned('out')) or move._is_int()) and move.with_company(move.company_id).product_id.cost_method == 'average'):
            product_tot_qty_available = move.product_id.sudo().with_company(move.company_id).quantity_svl + tmpl_dict[move.product_id.id]
            rounding = move.product_id.uom_id.rounding

            if move._is_out() and move._is_returned('out'):
                valued_move_lines = move._get_out_move_lines()

            elif move._is_int():
                valued_move_lines = move._get_int_move_lines()

            else:
                continue

            qty_done = 0
            for valued_move_line in valued_move_lines:
                qty_done += valued_move_line.product_uom_id._compute_quantity(valued_move_line.qty_done, move.product_id.uom_id)

            qty = forced_qty or qty_done
            if float_is_zero(product_tot_qty_available, precision_rounding=rounding):
                new_std_price = move._get_price_unit()
            elif float_is_zero(product_tot_qty_available + move.product_qty, precision_rounding=rounding) or \
                    float_is_zero(product_tot_qty_available + qty, precision_rounding=rounding):
                new_std_price = move._get_price_unit()
            else:
                amount_unit = std_price_update.get((move.company_id.id, move.product_id.id)) or move.product_id.with_company(move.company_id).standard_price

                if move._is_out() and move._is_returned('out'):
                    new_std_price = ((amount_unit * product_tot_qty_available) - (move._get_price_unit() * qty)) / (product_tot_qty_available - qty)

                elif move._is_int():
                    new_std_price = ((amount_unit * (product_tot_qty_available - qty)) + (move._get_price_unit() * qty)) / (product_tot_qty_available)

                else:
                    continue

            tmpl_dict[move.product_id.id] += qty_done
            move.product_id.with_company(move.company_id.id).with_context(disable_auto_svl=True).sudo().write({'standard_price': new_std_price})
            std_price_update[move.company_id.id, move.product_id.id] = new_std_price

        return res
