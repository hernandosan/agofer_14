# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    import_id = fields.Many2one('purchase.import', 'Import', copy=False)

    def action_generate_backorder_wizard(self):
        res = super(StockPicking, self).action_generate_backorder_wizard()
        if res.get('res_id') and self.import_id:
            self.env['stock.backorder.confirmation'].browse(res.get('res_id')).write({'imports_ids': [(4, p.id) for p in self.import_id]})
        return res

class StockMove(models.Model):
    _inherit = 'stock.move'

    import_id = fields.Many2one('purchase.import', 'Import', copy=False)
    import_percentage = fields.Float('Import Percentage', copy=False, default=0.0)

    def _action_done(self, cancel_backorder=False):
        # Init a dict that will group the moves by valuation type, according to `move._is_valued_type`.
        # valued_moves = {valued_type: self.env['stock.move'] for valued_type in self._get_valued_types()}
        valued_moves = {valued_type: self.env['stock.move'] for valued_type in self._get_valued_types()}
        for move in self:
            for valued_type in self._get_valued_types():
                if getattr(move, '_is_%s' % valued_type)():
                    valued_moves[valued_type] |= move
                    continue
        # Cost Import
        valued_moves['in'].price_unit_update_before_done()
        return super(StockMove, self)._action_done(cancel_backorder=cancel_backorder)

    def price_unit_update_before_done(self):
        moves = self.filtered(lambda m: m._is_in() and m.import_id)
        imports_ids = moves.import_id
        for purchase in imports_ids:
            amount_total = purchase._compute_amount_total()
            for move in moves.filtered(lambda m: m.import_id.id == purchase.id):
                cost = move.import_percentage * amount_total
                price_unit = move.price_unit + cost
                move.write({'price_unit': price_unit})

    def _get_price_unit(self):
        """ Returns the unit price for the move"""
        self.ensure_one()
        if self.purchase_line_id and self.product_id.id == self.purchase_line_id.product_id.id:
            """ Returns the unit price to value this stock move """
            price_unit = self.price_unit
            # If the move is a return, use the original move's price unit.
            if self.origin_returned_move_id and self.origin_returned_move_id.sudo().stock_valuation_layer_ids:
                price_unit = self.origin_returned_move_id.stock_valuation_layer_ids[-1].unit_cost
            return not self.company_id.currency_id.is_zero(price_unit) and price_unit or self.product_id.standard_price
        return super(StockMove, self)._get_price_unit()

    def _generate_valuation_lines_data(self, partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description):
        rslt = super(StockMove, self)._generate_valuation_lines_data(partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description)
        if self.import_id and self.import_id.moves_ids and self.purchase_line_id and self.product_id.id == self.purchase_line_id.product_id.id:
            price_unit = self._get_price_unit_purchase()
            qty_done = self.quantity_done
            value = price_unit * qty_done
            credit_line_vals = {
                'name': description,
                'product_id': self.product_id.id,
                'quantity': qty,
                'product_uom_id': self.product_id.uom_id.id,
                'ref': description,
                'partner_id': partner_id,
                'credit': value if credit_value > 0 else 0,
                'debit': value if credit_value < 0 else 0,
                'account_id': credit_account_id,
            }
            rslt.update(credit_line_vals=credit_line_vals)
            for invoice in self.import_id.moves_ids.filtered(lambda m: not m.import_bool):
                value = self.import_percentage * abs(invoice.amount_total_signed) * self.quantity_done
                dic = {
                    'name': description,
                    'product_id': self.product_id.id,
                    'quantity': qty,
                    'product_uom_id': self.product_id.uom_id.id,
                    'ref': description,
                    'partner_id': invoice.partner_id.id,
                    'credit': value if credit_value > 0 else 0,
                    'debit': value if credit_value < 0 else 0,
                    'account_id': credit_account_id,
                }
                name = 'credit_line_vals_' + str(invoice.id)
                rslt[name] = dic
        return rslt

    def _get_price_unit_purchase(self):
        """ Returns the unit price for the move"""
        self.ensure_one()
        line = self.purchase_line_id
        order = line.order_id
        price_unit = line.price_unit
        if line.taxes_id:
            price_unit = line.taxes_id.with_context(round=False).compute_all(price_unit, currency=line.order_id.currency_id, quantity=1.0)['total_void']
        if line.product_uom.id != line.product_id.uom_id.id:
            price_unit *= line.product_uom.factor / line.product_id.uom_id.factor
        if order.currency_id != order.company_id.currency_id:
            price_unit = order.currency_id._convert(
                price_unit, order.company_id.currency_id, order.company_id, fields.Date.context_today(self), round=False)
        return price_unit
