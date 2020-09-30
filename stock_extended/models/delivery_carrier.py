# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    name = fields.Char(required=False)
    carrier_type = fields.Selection([('stock','Stock'), ('purchase','Purchase')], 'Delivery Type', default='stock')
    partner_id = fields.Many2one('res.partner', 'Carrier')
    warehouse_id = fields.Many2one('stock.warehouse', 'Source Location')
    warehouse_dest_id = fields.Many2one('stock.warehouse', 'Destination Location')
    destination = fields.Char('Destination')
    price_kg = fields.Float('Price (Kg)')
    tolerance = fields.Float('Tolerance (%)', help='Tolerance allowed in price.')
    notes = fields.Text('Terms and Conditions')

    @api.model
    def create(self, vals):
        if vals.get('carrier_type') and vals.get('carrier_type') == 'stock':
            warehouse_id = self.env['stock.warehouse'].browse(vals.get('warehouse_id')).name or ''
            destination = vals.get('destination') or ''
            price = str(vals.get('fixed_price') or '')
            name = warehouse_id + ' -> ' + destination + ' $ ' + price
            vals.update(name=name)
        return super(DeliveryCarrier, self).create(vals)
    
    def write(self, vals):
        if vals.get('carrier_type') or vals.get('warehouse_id') or vals.get('destination') or vals.get('fixed_price'):
            for carrier in self:
                if vals.get('carrier_type') == 'stock' or carrier.carrier_type == 'stock':
                    warehouse_id = self.env['stock.warehouse'].browse(vals.get('warehouse_id')).name or carrier.warehouse_id.id
                    destination = vals.get('destination') or carrier.destination
                    price = str(vals.get('fixed_price') or carrier.fixed_price)
                    name = warehouse_id + ' -> ' + destination + ' $ ' + price
                    carrier.write({'name': name})
        return super(DeliveryCarrier, self).write(vals)
