# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    non_conforming_production_id = fields.Many2one('mrp.production', 'Production Order for non conforming', check_company=True, index=True)
