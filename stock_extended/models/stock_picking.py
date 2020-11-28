# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    incoterm = fields.Many2one('account.incoterms', 'Incoterm', help="International Commercial Terms are a series of predefined commercial terms used in international transactions.")
    shipping_type = fields.Selection([('delivery','Delivery Agofer'),('pick','Customer Pick')], 'Shipping Type', copy=False)
    pick_bool = fields.Boolean('Pick Bool')
    pick_date = fields.Date('Pick Date')
    upload_date = fields.Date('Upload Date')
    delivery_bool = fields.Boolean('Delivery Bool')
    delivery_assistant = fields.Boolean('Delivery Assistant')
    delivery_date = fields.Date('Delivery Date')
    warehouse_id = fields.Many2one(related='picking_type_id.warehouse_id', store=True)
    invoice_id = fields.Many2one('account.move', 'Invoice', readonly=True, copy=False)

    def action_invoice(self):
        for picking in self:
            picking._create_invoice()

    def _create_invoice(self):
        self.ensure_one()
        if self.sale_id:
            move = self.sale_id._create_invoices(final=True)[-1]
            if move:
                move.write({
                    'sale_id': self.sale_id.id if self.sale_id else False, 
                    'picking_id': self.id, 
                    'delivery_state': 'pending'
                })
                self.write({'invoice_id': move.id})
