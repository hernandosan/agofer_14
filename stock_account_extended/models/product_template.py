# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductPriceHistory(models.Model):
    _name = 'product.price.history'
    _description = 'Product price history'
    _rec_name = 'datetime'
    _order = 'datetime desc'

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    product_id = fields.Many2one('product.product', 'Product', required=True, ondelete='cascade')
    datetime = fields.Datetime('Historization Time', default=fields.Datetime.now())
    cost = fields.Float('Historized Cost', digits='Product Price')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self, vals):
        product = super(ProductProduct, self).create(vals)
        product.product_price_history(0.0)
        return product

    def write(self, vals):
        if 'standard_price' in vals:
             self.product_price_history(vals.get('standard_price') or 0.0)
        return super(ProductProduct, self).write(vals)

    def product_price_history(self, value):
        for product in self:
            self.env['product.price.history'].create({
                'product_id': product.id,
                'cost': value
            })

    def _prepare_in_returned_svl_vals(self, quantity, unit_cost, company):
        """Prepare the values for a stock valuation layer created by a delivery.

        :param quantity: the quantity to value, expressed in `self.uom_id`
        :return: values to use in a call to create
        :rtype: dict
        """
        self.ensure_one()
        # Quantity is negative for out valuation layers.
        quantity = -1 * quantity
        vals = {
            'product_id': self.id,
            'value': unit_cost * quantity,
            'unit_cost': unit_cost,
            'quantity': quantity,
        }
        if self.cost_method in ('average', 'fifo'):
            fifo_vals = self._run_fifo(abs(quantity), company)
            vals['remaining_qty'] = fifo_vals.get('remaining_qty')
            if self.cost_method == 'fifo':
                vals.update(fifo_vals)
        return vals

    def _prepare_out_returned_svl_vals(self, quantity, unit_cost):
        """Prepare the values for a stock valuation layer created by a receipt.

        :param quantity: the quantity to value, expressed in `self.uom_id`
        :param unit_cost: the unit cost to value `quantity`
        :return: values to use in a call to create
        :rtype: dict
        """
        self.ensure_one()
        vals = {
            'product_id': self.id,
            'value': unit_cost * quantity,
            'unit_cost': unit_cost,
            'quantity': quantity,
        }
        if self.cost_method in ('average', 'fifo'):
            vals['remaining_qty'] = quantity
            vals['remaining_value'] = vals['value']
        return vals
