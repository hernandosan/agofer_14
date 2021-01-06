# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        self.action_before_validate()
        return super(StockPicking, self).button_validate()

    def do_print_picking(self):
        self.action_before_validate()
        return super(StockPicking, self).do_print_picking()

    def action_before_validate(self):
        for picking in self.filtered(lambda p: p.picking_type_code == 'outgoing' and p.sale_id):
            picking._action_before_validate()

    def _action_before_validate(self):
        self.ensure_one()
        sale_id = self.sale_id.filtered(lambda s: s.credit_type == 'cash')
        sale_id.with_context({'state': 'posted'}).validate_cash_control()
