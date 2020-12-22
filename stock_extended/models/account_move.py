# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    guides_ids = fields.Many2many('delivery.guide', 'guide_invoice_rel', 'invoice_id', 'guide_id', 'Guides', copy=False)
    guides_returns_ids = fields.Many2many('delivery.guide', 'guide_invoice_return_rel', 'invoice_id', 'guide_id', 'Guides Return', copy=False)

    def action_guide_confirm(self):
        for move in self:
            move._action_guide_confirm()

    def action_guide_return(self):
        if self._context.get('delivery_guide'):
            self.env['delivery.guide'].browse(self._context.get('delivery_guide')).write({'guide_bool': True})
        self.write({'delivery_state': 'novelty'})

    def _action_guide_confirm(self):
        self.ensure_one()
        if self.move_type == 'out_invoice':
            guides_ids = self.guides_ids.filtered(lambda g: g.state in ('draft','confirm','progress'))
            if len(guides_ids) > 1:
                return self.write({'delivery_state': 'partial'})
        if self.move_type == 'out_refund':
            guides_ids = self.guides_returns_ids.filtered(lambda g: g.state in ('draft','confirm','progress'))
            if len(guides_ids) > 1:
                return self.write({'delivery_state': 'partial'})
        return self.write({'delivery_state': 'delivered'})
