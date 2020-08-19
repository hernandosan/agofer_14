# -*- coding: utf-8 -*-

from collections import defaultdict

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round, float_is_zero

import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def _get_valued_types_returned(self):
        """Returns a list of `valued_type` as strings. During `action_done`, we'll call
        `_is_[valued_type]'. If the result of this method is truthy, we'll consider the move to be
        valued.

        :returns: a list of `valued_type`
        :rtype: list
        """
        return ['in_returned', 'out_returned']

    def _get_in_returned_move_lines(self):
        """ Returns the `stock.move.line` records of `self` considered as incoming returned. It is done thanks
        to the `_should_be_valued` method of their source and destionation location as well as their
        owner.

        :returns: a subset of `self` containing the incoming records
        :rtype: recordset
        """
        self.ensure_one()
        res = self.env['stock.move.line']
        if self.origin_returned_move_id:
            for move_line in self.move_line_ids:
                if move_line.owner_id and move_line.owner_id != move_line.company_id.partner_id:
                    continue
                if move_line.location_id._should_be_valued() and not move_line.location_dest_id._should_be_valued():
                    res |= move_line
        return res

    def _is_in_returned(self):
        """Check if the move should be considered as entering the company so that the cost method
        will be able to apply the correct logic.

        :returns: True if the move is entering the company else False
        :rtype: bool
        """
        self.ensure_one()
        if self._get_in_returned_move_lines():
            return True
        return False

    def _get_out_returned_move_lines(self):
        """ Returns the `stock.move.line` records of `self` considered as outgoing. It is done thanks
        to the `_should_be_valued` method of their source and destionation location as well as their
        owner.

        :returns: a subset of `self` containing the outgoing records
        :rtype: recordset
        """
        res = self.env['stock.move.line']
        if self.origin_returned_move_id:
            for move_line in self.move_line_ids:
                if move_line.owner_id and move_line.owner_id != move_line.company_id.partner_id:
                    continue
                if not move_line.location_id._should_be_valued() and move_line.location_dest_id._should_be_valued():
                    res |= move_line
            return res

    def _is_out_returned(self):
        """Check if the move should be considered as leaving the company so that the cost method
        will be able to apply the correct logic.

        :returns: True if the move is leaving the company else False
        :rtype: bool
        """
        self.ensure_one()
        if self._get_out_returned_move_lines():
            return True
        return False

    def _action_done(self, cancel_backorder=False):
        # Init a dict that will group the moves by valuation type, according to `move._is_valued_type`.
        # valued_moves = {valued_type: self.env['stock.move'] for valued_type in self._get_valued_types()}
        valued_moves = {valued_type: self.env['stock.move'] for valued_type in self._get_valued_types_returned()}
        for move in self:
            for valued_type in self._get_valued_types_returned():
                if getattr(move, '_is_%s' % valued_type)():
                    valued_moves[valued_type] |= move
                    continue

        # AVCO application
        valued_moves['in_returned'].product_price_update_before_done_returned()
        return super(StockMove, self)._action_done(cancel_backorder=cancel_backorder)
    
    def product_price_update_before_done_returned(self, forced_qty=None):
        tmpl_dict = defaultdict(lambda: 0.0)
        # adapt standard price on incomming moves if the product cost_method is 'average'
        std_price_update = {}
        for move in self.filtered(lambda move: move._is_in_returned() and move.with_context(force_company=move.company_id.id).product_id.cost_method == 'average'):
            product_tot_qty_available = move.product_id.sudo().with_context(force_company=move.company_id.id).quantity_svl + tmpl_dict[move.product_id.id]
            rounding = move.product_id.uom_id.rounding

            valued_move_lines = move._get_in_returned_move_lines()
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
                # Get the standard price
                amount_unit = std_price_update.get((move.company_id.id, move.product_id.id)) or move.product_id.with_context(force_company=move.company_id.id).standard_price
                new_std_price = ((amount_unit * product_tot_qty_available) - (move._get_price_unit() * qty)) / (product_tot_qty_available - qty)

            tmpl_dict[move.product_id.id] += qty_done
            # Write the standard price, as SUPERUSER_ID because a warehouse manager may not have the right to write on products
            move.product_id.with_context(force_company=move.company_id.id).sudo().write({'standard_price': new_std_price})
            std_price_update[move.company_id.id, move.product_id.id] = new_std_price
