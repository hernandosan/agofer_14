# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    carrier_id = fields.Many2one('delivery.carrier', 'Carrier', check_company=True, states={'done': [('readonly', True)]})
    carrier_partner_id = fields.Many2one('res.partner', 'Transporter', states={'done': [('readonly', True)]})
    landed_type = fields.Selection([('stock','Stock'), ('purchase','Purchase')], 'Landed Type', default='stock')


class StockLandedCostLines(models.Model):
    _inherit = 'stock.landed.cost.lines'

    product_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1)
    price = fields.Float(string='Unit Price', required=True, digits='Product Price')

    @api.onchange('product_qty', 'price')
    def _onchange_price_unit(self):
        self.price_unit = self.product_qty * self.price if self.product_qty and self.price else self.price_unit

