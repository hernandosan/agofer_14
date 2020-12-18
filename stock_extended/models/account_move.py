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
        return True

    def _action_guide_confirm(self):
        self.ensure_one()
        if len(self.guides_ids) > 1:
            print('Holis')
