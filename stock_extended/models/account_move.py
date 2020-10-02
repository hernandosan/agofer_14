# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    picking_id = fields.Many2one('stock.picking', readonly=True, copy=False)
    guides_ids = fields.Many2many('delivery.guide', 'guide_invoice_rel', 'invoice_id', 'guide_id', 'Guides', copy=False)
    delivery_state = fields.Selection([('pending','Pending'),('progress','Progress'),('delivered','Delivered')], 'Delivery state', copy=False)
