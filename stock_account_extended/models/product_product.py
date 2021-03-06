# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _prepare_int_svl_vals(self, quantity, unit_cost):
        self.ensure_one()
        vals = {
            'product_id': self.id,
            'value': unit_cost * quantity,
            'unit_cost': 0.0,
            'quantity': 0.0,
            'remaining_qty': 0.0
        }
        if self.cost_method in ('average', 'fifo'):
            vals['remaining_qty'] = quantity
            vals['remaining_value'] = vals['value']
        return vals
