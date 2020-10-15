# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    picking_id = fields.Many2one('stock.picking', readonly=True, copy=False)
    guides_ids = fields.Many2many('delivery.guide', 'guide_invoice_rel', 'invoice_id', 'guide_id', 'Guides', copy=False)
    delivery_state = fields.Selection([
        ('pending','Pending'),
        ('progress','Progress'),
        ('return','Return'),
        ('delivered','Delivered')], 'Delivery state', copy=False)

    def action_delivery_confirm(self):
        self.write({'delivery_state': 'delivered'})

    def action_delivery_return(self):
        self.guides_ids.write({'guide_bool': True})
        self.write({'delivery_state': 'return'})
