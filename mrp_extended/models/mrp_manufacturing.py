# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MrpManufacturing(models.Model):
    _name = 'mrp.manufacturing'
    _description = 'Manufacturing Order'

    name = fields.Char('Name', required=True)

    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.company)

    product_id = fields.Many2one('product.product', 'Product', required=True, tracking=True)
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    product_uom_id = fields.Many2one('uom.uom', 'Unit of Measure', readonly=True, required=True)

    qty_product = fields.Float('Quantity Available', digits='Product Unit of Measure')
    qty_production = fields.Float('Quantity Production', digits='Product Unit of Measure')

    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user)

    workcenter_id = fields.Many2one('mrp.workcenter', 'Workcenter', ondelete="restric")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.update({
            'product_uom_id': self.product_id.uom_id.id if self.product_id else self.product_uom_id,
        })
