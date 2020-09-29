# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    pricelists_ids = fields.Many2many('product.pricelist', 'warehouse_pricelist_rel', 'warehouse_id', 'pricelist_id', 'Pricelists')
