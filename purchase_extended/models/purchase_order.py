# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    imports_ids = fields.Many2many('purchase.import', 'import_order_rel', 'order_id', 'import_id', 'Imports', copy=False)
