# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    picking_id = fields.Many2one('stock.picking', readonly=True, copy=False)
    delivery_state = fields.Selection([
        ('pending','Pending'),
        ('progress','Progress'),
        ('cancel','Cancel'),
        ('delivered','Delivered')], 'Delivery state', copy=False)

    def action_delivery_confirm(self):
        for move in self:
            move._action_delivery('delivered')

    def action_delivery_cancel(self):
        for move in self:
            move._action_delivery('cancel')

    def _action_delivery(self, state):
        self.ensure_one()
        self.write({'delivery_state': state})
