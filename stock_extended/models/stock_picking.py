# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


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
    # Print
    print_picking = fields.Boolean('Printed', copy=False)
    print_user_id = fields.Many2one('res.users', 'Print User', copy=False)
    # Sale
    sale_invoice_status = fields.Selection(related='sale_id.invoice_status')
    # Shipping
    shipping_type = fields.Selection([('delivery','Delivery Agofer'),('pick','Customer Pick')], 'Shipping Type', copy=False)
    # Upload
    upload_date = fields.Date('Upload Date')
    # Warehouse
    warehouse_id = fields.Many2one(related='picking_type_id.warehouse_id', store=True)

    def do_print_picking(self):
        self.check_printed_picking()
        return super(StockPicking, self).do_print_picking()

    def printed_picking(self):
        self.check_printed_picking()
        self.write({'print_picking': True, 'print_user_id': self.env.user.id})
        return True

    def check_printed_picking(self):
        for picking in self:
            picking._check_printed_picking()

    def _check_printed_picking(self):
        self.ensure_one()
        if self.print_picking:
            raise ValidationError("The picking %s has already been printed" % self.name)
        return True
