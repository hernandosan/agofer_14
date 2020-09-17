# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    discount_maximum = fields.Float('Maximum percentage', default=10, help='Maximum discount allowed in the order')
    discount_freight = fields.Float('Freight percentage', default=2, help='Maximum discount allowed when the customer collects')


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    @api.model
    def create(self, vals):
        item = super(ProductPricelistItem, self).create(vals)
        item.product_pricelist_history(vals.get('fixed_price') or 0.0)
        return item

    def write(self, vals):
        if 'fixed_price' in vals:
             self.product_pricelist_history(vals.get('fixed_price') or 0.0)
        return super(ProductPricelistItem, self).write(vals)

    def product_pricelist_history(self, value):
        for item in self:
            self.env['product.pricelist.history'].create({
                'item_id': item.id,
                'price': value
            })


class ProductPricelistHistory(models.Model):
    _name = 'product.pricelist.history'
    _description = 'Product pricelist history'
    _rec_name = 'datetime'
    _order = 'datetime desc'

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    item_id = fields.Many2one('product.pricelist.item', 'Item', required=True, ondelete='cascade')
    datetime = fields.Datetime('Historization Time', default=fields.Datetime.now())
    price = fields.Float('Historized Price', digits='Product Price')
