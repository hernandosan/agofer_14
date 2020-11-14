# -*- coding: utf-8 -*-

from collections import defaultdict

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round, float_is_zero

import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    standard_price = fields.Float('Cost', digits='Product Price')
    cost_id = fields.Many2one('stock.landed.cost', 'Landed Cost')
    additional_cost = fields.Float('Additional Landed Cost', digits='Account')

    # @api.model
    # def create(self, vals):
    #     standard_price = self.env['product.product'].browse(vals['product_id']).standard_price
    #     vals.update(price_unit=standard_price)
    #     return super(StockMove, self).create(vals)

    @api.model
    def _get_valued_types(self):
        """Returns a list of `valued_type` as strings. During `action_done`, we'll call
        `_is_[valued_type]'. If the result of this method is truthy, we'll consider the move to be
        valued.

        :returns: a list of `valued_type`
        :rtype: list
        """
        res = super(StockMove, self)._get_valued_types()
        res.append('int')
        res.append('in_returned')
        res.append('out_returned')
        return res

    def _get_in_move_lines(self):
        """ Returns the `stock.move.line` records of `self` considered as incoming. It is done thanks
        to the `_should_be_valued` method of their source and destionation location as well as their
        owner.

        :returns: a subset of `self` containing the incoming records
        :rtype: recordset
        """
        res = super(StockMove, self)._get_in_move_lines()
        return self.env['stock.move.line'] if self.origin_returned_move_id else res

    def _get_out_move_lines(self):
        """ Returns the `stock.move.line` records of `self` considered as outgoing. It is done thanks
        to the `_should_be_valued` method of their source and destionation location as well as their
        owner.

        :returns: a subset of `self` containing the outgoing records
        :rtype: recordset
        """
        res = super(StockMove, self)._get_out_move_lines()
        return self.env['stock.move.line'] if self.origin_returned_move_id else res

    def _create_int_svl(self, forced_quantity=None):
        """Create a `stock.valuation.layer` from `self`.

        :param forced_quantity: under some circunstances, the quantity to value is different than
            the initial demand of the move (Default value = None)
        """
        svl_vals_list = []
        for move in self:
            move = move.with_company(move.company_id)
            valued_move_lines = move._get_int_move_lines()
            valued_quantity = 0
            for valued_move_line in valued_move_lines:
                valued_quantity += valued_move_line.product_uom_id._compute_quantity(valued_move_line.qty_done, move.product_id.uom_id)
            # unit_cost = abs(move._get_price_unit())  # May be negative (i.e. decrease an out move).
            unit_cost = move.additional_cost / valued_quantity
            if move.product_id.cost_method == 'standard':
                unit_cost = move.product_id.standard_price
            svl_vals = move.product_id._prepare_int_svl_vals(forced_quantity or valued_quantity, unit_cost)
            svl_vals.update(move._prepare_common_svl_vals())
            if forced_quantity:
                svl_vals['description'] = 'Correction of %s (modification of past move)' % move.picking_id.name or move.name
            # Add stock landed cost
            svl_vals.update(stock_landed_cost_id=move.cost_id.id)
            svl_vals_list.append(svl_vals)
        return self.env['stock.valuation.layer'].sudo().create(svl_vals_list)

    def _get_int_move_lines(self):
        """ Returns the `stock.move.line` records of `self` considered as internal. It is done thanks
        to the `_should_be_valued` method of their source and destionation location as well as their
        owner.

        :returns: a subset of `self` containing the incoming records
        :rtype: recordset
        """
        self.ensure_one()
        res = self.env['stock.move.line']
        for move_line in self.filtered(lambda m: m.cost_id).move_line_ids:
            if move_line.owner_id and move_line.owner_id != move_line.company_id.partner_id:
                continue
            if move_line.location_id._should_be_valued() and move_line.location_dest_id._should_be_valued():
                res |= move_line
        return res

    def _is_int(self):
        """Check if the move should be considered as entering the company so that the cost method
        will be able to apply the correct logic.

        :returns: True if the move is internal the company else False
        :rtype: bool
        """
        self.ensure_one()
        if self._get_int_move_lines():
            return True
        return False

    def _create_in_returned_svl(self, forced_quantity=None):
        """Create a `stock.valuation.layer` from `self`.

        :param forced_quantity: under some circunstances, the quantity to value is different than
            the initial demand of the move (Default value = None)
        """
        svl_vals_list = []
        for move in self:
            move = move.with_context(force_company=move.company_id.id)
            valued_move_lines = move._get_in_returned_move_lines()
            valued_quantity = 0
            for valued_move_line in valued_move_lines:
                valued_quantity += valued_move_line.product_uom_id._compute_quantity(valued_move_line.qty_done, move.product_id.uom_id)
            if float_is_zero(forced_quantity or valued_quantity, precision_rounding=move.product_id.uom_id.rounding):
                continue
            unit_cost = abs(move._get_price_unit())  # May be negative (i.e. decrease an out move).
            if move.product_id.cost_method == 'standard':
                unit_cost = move.product_id.standard_price
            svl_vals = move.product_id._prepare_in_returned_svl_vals(forced_quantity or valued_quantity, unit_cost, move.company_id)
            svl_vals.update(move._prepare_common_svl_vals())
            if forced_quantity:
                svl_vals['description'] = 'Correction of %s (modification of past move)' % move.picking_id.name or move.name
            svl_vals_list.append(svl_vals)
        return self.env['stock.valuation.layer'].sudo().create(svl_vals_list)

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

    def _create_out_returned_svl(self, forced_quantity=None):
        """Create a `stock.valuation.layer` from `self`.

        :param forced_quantity: under some circunstances, the quantity to value is different than
            the initial demand of the move (Default value = None)
        """
        svl_vals_list = []
        for move in self:
            move = move.with_context(force_company=move.company_id.id)
            valued_move_lines = move._get_out_returned_move_lines()
            valued_quantity = 0
            for valued_move_line in valued_move_lines:
                valued_quantity += valued_move_line.product_uom_id._compute_quantity(valued_move_line.qty_done, move.product_id.uom_id)
            unit_cost = abs(move._get_price_unit())  # May be negative (i.e. decrease an out move).
            if move.product_id.cost_method == 'standard':
                unit_cost = move.product_id.standard_price
            svl_vals = move.product_id._prepare_out_returned_svl_vals(forced_quantity or valued_quantity, unit_cost)
            svl_vals.update(move._prepare_common_svl_vals())
            if forced_quantity:
                svl_vals['description'] = 'Correction of %s (modification of past move)' % move.picking_id.name or move.name
            svl_vals_list.append(svl_vals)
        return self.env['stock.valuation.layer'].sudo().create(svl_vals_list)

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
        valued_moves = {valued_type: self.env['stock.move'] for valued_type in self._get_valued_types()}
        for move in self:
            for valued_type in self._get_valued_types():
                if getattr(move, '_is_%s' % valued_type)():
                    valued_moves[valued_type] |= move
                    continue

        # AVCO application
        valued_moves['int'].product_price_update_before_done_extended()
        valued_moves['in_returned'].product_price_update_before_done_extended()
        valued_moves['out_returned'].product_price_update_before_done_extended()
        res = super(StockMove, self)._action_done(cancel_backorder=cancel_backorder)
        self.standard_price_update_after_done_extended()
        return res

    def product_price_update_before_done_extended(self, forced_qty=None):
        tmpl_dict = defaultdict(lambda: 0.0)
        # adapt standard price on incomming moves if the product cost_method is 'average'
        std_price_update = {}
        for move in self.filtered(lambda move: move._is_int() or move._is_in_returned() or move._is_out_returned() and move.with_company(move.company_id).product_id.cost_method == 'average'):
            product_tot_qty_available = move.product_id.sudo().with_company(move.company_id).quantity_svl + tmpl_dict[move.product_id.id]
            rounding = move.product_id.uom_id.rounding

            if move._is_int():
                valued_move_lines = move._get_int_move_lines()
            elif move._is_in_returned():
                valued_move_lines = move._get_in_returned_move_lines()
            else:
                valued_move_lines = move._get_out_returned_move_lines()

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
                amount_unit = std_price_update.get((move.company_id.id, move.product_id.id)) or move.product_id.with_company(move.company_id).standard_price
                if move._is_int():
                    new_std_price = ((amount_unit * (product_tot_qty_available - qty)) + (move._get_price_unit() * qty)) / (product_tot_qty_available)
                elif move._is_in_returned():
                    new_std_price = ((amount_unit * product_tot_qty_available) - (move._get_price_unit() * qty)) / (product_tot_qty_available - qty)
                else:
                    new_std_price = ((amount_unit * product_tot_qty_available) + (move._get_price_unit() * qty)) / (product_tot_qty_available + qty)

            tmpl_dict[move.product_id.id] += qty_done
            # Write the standard price, as SUPERUSER_ID because a warehouse manager may not have the right to write on products
            move.product_id.with_company(move.company_id.id).with_context(disable_auto_svl=True).sudo().write({'standard_price': new_std_price})
            std_price_update[move.company_id.id, move.product_id.id] = new_std_price

    def standard_price_update_after_done_extended(self):
        for move in self:
            move.write({'standard_price': move.product_id.standard_price})

    def _account_entry_move(self, qty, description, svl_id, cost):
        """ Accounting Valuation Entries """
        self.ensure_one()
        if self.product_id.type != 'product':
            # no stock valuation for consumable products
            return False
        if self.restrict_partner_id:
            # if the move isn't owned by the company, we don't make any valuation
            return False

        location_from = self.location_id
        location_to = self.location_dest_id
        company_from = self._is_in_returned() and self.mapped('move_line_ids.location_id.company_id') or False
        company_to = self._is_out_returned() and self.mapped('move_line_ids.location_dest_id.company_id') or False

        journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()

        # Create Journal Entry for moves internal
        if self._is_int():
            company_to = self.mapped('move_line_ids.location_dest_id.company_id') or company_to
            journal_id = self.cost_id.account_journal_id.id if self.cost_id and self.cost_id.account_journal_id else journal_id
            self.with_company(company_to)._create_account_move_line(acc_src, acc_valuation, journal_id, qty, description, svl_id, cost)

        # Create Journal Entry for products arriving in the company; in case of routes making the link between several
        # warehouse of the same company, the transit location belongs to this company, so we don't need to create accounting entries
        if self._is_out_returned():
            self.with_company(company_to)._create_account_move_line(acc_src, acc_valuation, journal_id, qty, description, svl_id, cost)

        # Create Journal Entry for products leaving the company
        if self._is_in_returned():
            cost = -1 * cost
            self.with_company(company_from)._create_account_move_line(acc_valuation, acc_dest, journal_id, qty, description, svl_id, cost)

        return super(StockMove, self)._account_entry_move(qty=qty, description=description, svl_id=svl_id, cost=cost)
