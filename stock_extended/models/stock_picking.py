# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

selection_type_vehicle = [
    ('automobile', 'Automobile'),
    ('carry', 'Carry'),
    ('minimule', 'Minimule'),
    ('pedestrian', 'Pedestrian'),
    ('simple', 'Simple'),
    ('tractomule', 'Tractomule'),
    ('truck', 'Truck'),
    ('turbo', 'Turbo'),
    ('wheelbarrow', 'Wheelbarrow'),
]

selection_condition_vehicle = [
    ('bodywork', 'Bodywork'),
    ('not_apply', 'Not apply'),
    ('slab', 'Slab'),
    ('van', 'Van')
]


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # Carrier
    carrier_partner_id = fields.Many2one('res.partner', 'Transporter')
    # Delivery
    delivery_assistant = fields.Boolean('Delivery Assistant')
    delivery_bool = fields.Boolean('Delivery Bool')
    delivery_date = fields.Date('Delivery Date')
    # Driver
    driver_id = fields.Many2one('res.partner', 'Driver')
    # Incoterm
    incoterm = fields.Many2one('account.incoterms', 'Incoterm', 
        help="International Commercial Terms are a series of predefined commercial terms used in international transactions.")
    # Pïck
    pick_file = fields.Binary('Authorization Pick')
    pick_file_name = fields.Char('Authorization Pick Name')
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
    shipping_type_vehicle = fields.Selection(selection_type_vehicle, 'Vehicle Type')
    shipping_type_condition = fields.Selection(selection_condition_vehicle, 'Vehicle Condition')
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
        self.action_before_print()
        return super(StockPicking, self).do_print_picking()

    def action_before_print(self):
        self.printed_picking()
        self.checked_state()

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

    def checked_state(self):
        for picking in self:
            picking._checked_state()

    def _checked_state(self):
        self.ensure_one()
        if self.state != 'assigned' and not self.env.user.has_group('stock.group_stock_manager'):
            raise ValidationError(_("You cannot print the picking %s" % self.name))
