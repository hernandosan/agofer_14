# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    imports_ids = fields.Many2many('purchase.import', 'import_order_rel', 'order_id', 'import_id', 'Imports', copy=False)
    import_bool = fields.Boolean('Import Bool', copy=False)

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        self.action_purchase_import()
        return res

    def action_purchase_import(self):
        for order in self:
            check_country = False if order.partner_id.country_id != self.env.company.partner_id.country_id else True
            order.write({'import_bool': True}) if order.picking_ids.filtered(lambda p: p.state == 'assigned') and not check_country else order.write({'import_bool': False})
