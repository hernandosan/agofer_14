# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    import_id = fields.Many2one('purchase.import', 'Import', copy=False)
