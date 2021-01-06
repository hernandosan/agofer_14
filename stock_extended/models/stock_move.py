# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    def action_assign_done(self):
        for move in self.filtered(lambda move: move.state not in ('draft', 'cancel', 'done')):
            move._action_assign_done()

    def _action_assign_done(self):
        self.ensure_one()
        self.write({'quantity_done': self.reserved_availability})
