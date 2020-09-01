# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    import_id = fields.Many2one('purchase.import', 'Import', copy=False)


class StockMove(models.Model):
    _inherit = 'stock.move'

    import_id = fields.Many2one('purchase.import', 'Import', copy=False)
