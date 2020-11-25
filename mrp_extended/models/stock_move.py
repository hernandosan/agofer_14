# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    production_second_id = fields.Many2one('mrp.production', 'Production Order for second finished products ', check_company=True, index=True)
    production_decrease_id = fields.Many2one('mrp.production', 'Production Order for decrease finished products', check_company=True, index=True)
