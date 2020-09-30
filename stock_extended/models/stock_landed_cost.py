# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    landed_type = fields.Selection([('stock','Stock'), ('purchase','Purchase')], 'Landed Type', default='stock')
    carrier_id = fields.Many2one('delivery.carrier', 'Carrier', check_company=True, states={'done': [('readonly', True)]})
