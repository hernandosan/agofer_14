# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # Carrier
    carrier_partner_id = fields.Many2one('res.partner', 'Transporter')
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
    pick_name = fields.Char('Pick Name')
    pick_vat = fields.Char('Pick VAT')
    pick_license = fields.Char('Pick License')
    pick_risk = fields.Char('Pick Risk')
    # Print
    print_picking = fields.Boolean('Picking Printed', copy=False)
    print_user_id = fields.Many2one('res.users', 'User Print', copy=False)
    # Sale
    sale_invoice_status = fields.Selection(related='sale_id.invoice_status')
    # Shipping
    shipping_type = fields.Selection([('delivery','Delivery Agofer'),('pick','Customer Pick')], 'Shipping Type')
    # Upload
    upload_date = fields.Date('Upload Date')
    # Warehouse
    warehouse_id = fields.Many2one(related='picking_type_id.warehouse_id', store=True)

    def write(self, values):
        if values.get('shipping_type') and values.get('shipping_type') == 'delivery':
            self.check_shipping_type()
        return super().write(values)

    def action_assign(self):
        res = super(StockPicking, self).action_assign()
        self.filtered(lambda s: s.sale_id).mapped('move_lines').action_assign_done()
        return res

    def do_print_picking(self):
        self.printed_picking()
        return super(StockPicking, self).do_print_picking()

    def printed_picking(self):
        for picking in self:
            picking._check_printed_picking()
            picking._printed_picking()

    def _printed_picking(self):
        self.ensure_one()
        if not self.print_picking:
            self.write({'print_picking': True})
        if not self.print_user_id:
            self.write({'print_user_id': self.env.user.id})

    def check_printed_picking(self):
        for picking in self:
            picking._check_printed_picking()

    def _check_printed_picking(self):
        self.ensure_one()
        if self.print_picking and not self.env.user.has_group('stock.group_stock_manager'):
            raise ValidationError(_("The picking %s has already been printed") % self.name)
        return True

    def check_shipping_type(self):
        for picking in self.filtered(lambda p: p.shipping_type):
            picking._check_shipping_type()

    def _check_shipping_type(self):
        self.ensure_one()
        if self.shipping_type == 'pick' and (not self.env.user.has_group('stock.group_stock_manager') or not self.env.user.has_group('sales_team.group_sale_manager')):
            raise ValidationError(_("You cannot change the shipping type in picking %s" % self.name))
