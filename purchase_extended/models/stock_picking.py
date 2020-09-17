# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


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

    categ_id = fields.Many2one(related='product_id.categ_id', store=True)
    import_id = fields.Many2one('purchase.import', 'Import', copy=False)
    import_done_id = fields.Many2one('purchase.import', 'Import Done', copy=False)
    import_percentage = fields.Float('Import Percentage', copy=False, default=0.0)
    import_line_id = fields.Many2one('purchase.import.line', 'Import Line', copy=False)

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
        for move in moves:
            line_id = move.import_id.import_line.filtered(lambda l: l.move_id and l.move_id.id == move.id)
            if line_id:
                price_subtotal = line_id.price_subtotal
                price_unit = price_subtotal / move.quantity_done
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
            line_id = self.import_id.import_line.filtered(lambda l: l.move_id and l.move_id.id == self.id)
            if line_id:
                decimal_places = line_id.currency_id.decimal_places
                credit_value = round(line_id.price_cif, decimal_places)
                credit_line_vals = {
                    'name': description,
                    'product_id': self.product_id.id,
                    'quantity': qty,
                    'product_uom_id': self.product_id.uom_id.id,
                    'ref': description,
                    'partner_id': partner_id,
                    'credit': credit_value if credit_value > 0 else 0,
                    'debit': credit_value if credit_value < 0 else 0,
                    'account_id': credit_account_id,
                }
                rslt.update(credit_line_vals=credit_line_vals)
                for invoice in self.import_id.moves_ids.filtered(lambda m: m.import_type and m.import_type != 'vat'):
                    value = self.import_percentage * abs(invoice.amount_total_signed) if invoice.import_type != 'tariff' else line_id.price_tariff
                    value = round(value, decimal_places)
                    credit_value += value
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
                if round(debit_value - credit_value, decimal_places) != 0.0:
                    if rslt.get('price_diff_line_vals'):
                        diff_amount = debit_value - credit_value
                        price_diff_account = self.product_id.property_account_creditor_price_difference
                        price_diff_line_vals = {
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
                        rslt.update(price_diff_line_vals=price_diff_line_vals)
                    else:
                        debit_value = credit_value
                        debit_line_vals = {
                            'name': description,
                            'product_id': self.product_id.id,
                            'quantity': qty,
                            'product_uom_id': self.product_id.uom_id.id,
                            'ref': description,
                            'partner_id': partner_id,
                            'debit': debit_value if debit_value > 0 else 0,
                            'credit': -debit_value if debit_value < 0 else 0,
                            'account_id': debit_account_id,
                        }
                        rslt.update(debit_line_vals=debit_line_vals)
        return rslt

    def _get_price_unit_purchase(self):
        """ Returns the unit price for the move"""
        self.ensure_one()
        line = self.purchase_line_id
        order = line.order_id
        purchase = self.import_id
        price_unit = line.price_unit
        if line.taxes_id:
            price_unit = line.taxes_id.with_context(round=False).compute_all(price_unit, currency=line.order_id.currency_id, quantity=1.0)['total_void']
        if line.product_uom.id != line.product_id.uom_id.id:
            price_unit *= line.product_uom.factor / line.product_id.uom_id.factor
        if order.currency_id != order.company_id.currency_id:
            if order.currency_id != purchase.currency_id:
                raise ValidationError(_("Currency of the import order is different to currency of the purchase order"))
            price_unit = order.currency_id.with_context(date=purchase.date_import).compute(price_unit, purchase.currency_company_id)
        return price_unit
