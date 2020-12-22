# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # Delivery
    delivery_assistant = fields.Boolean('Delivery Assistant')
    delivery_bool = fields.Boolean('Delivery Bool')
    delivery_date = fields.Date('Delivery Date')
    # Incoterm
    incoterm = fields.Many2one('account.incoterms', 'Incoterm', 
        help="International Commercial Terms are a series of predefined commercial terms used in international transactions.")
    # Pïck
    pick_bool = fields.Boolean('Pick Bool')
    pick_date = fields.Date('Pick Date')
    # Sale
    sale_invoice_status = fields.Selection(related='sale_id.invoice_status')
    # Shipping
    shipping_type = fields.Selection([('delivery','Delivery Agofer'),('pick','Customer Pick')], 'Shipping Type', copy=False)
    # Upload
    upload_date = fields.Date('Upload Date')
    # Warehouse
    warehouse_id = fields.Many2one(related='picking_type_id.warehouse_id', store=True)
