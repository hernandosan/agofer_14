# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    product_id = fields.Many2one('product.product', 'Product', domain="[('type', '=', 'service')]")
    sequence_id = fields.Many2one('ir.sequence', 'Sequence')
