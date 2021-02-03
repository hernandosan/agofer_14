# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    name = fields.Char(required=False)
    carrier_type = fields.Selection([('stock','Stock'), ('purchase','Purchase')], 'Delivery Type', default='stock')
    partner_id = fields.Many2one('res.partner', 'Carrier')
    warehouse_id = fields.Many2one('res.city', 'Source Location')
    warehouse_dest_id = fields.Many2one('res.city', 'Destination Location')
    # destination = fields.Char('Destination')
    price_kg = fields.Float('Price (Kg)')
    tolerance = fields.Float('Tolerance (%)', help='Tolerance allowed in price.')
    notes = fields.Text('Terms and Conditions')

    @api.model
    def create(self, vals):
        if vals.get('carrier_type') and vals.get('carrier_type') == 'stock':
            warehouse_id = self.env['res.city'].browse(vals.get('warehouse_id')).name or ''
            warehouse_dest_id = self.env['res.city'].browse(vals.get('warehouse_dest_id')).name or ''
            price = str(vals.get('price_kg') or '')
            name = '%s -> %s $ %s' % (warehouse_id, warehouse_dest_id, price)
            vals.update(name=name)
        return super(DeliveryCarrier, self).create(vals)

    def write(self, vals):
        if vals.get('carrier_type') or vals.get('city_id') or vals.get('price_kg'):
            for carrier in self:
                if vals.get('carrier_type') == 'stock' or carrier.carrier_type == 'stock':
                    warehouse_id = self.env['res.city'].browse(vals.get('warehouse_id')) or carrier.city_id.id
                    warehouse_dest_id = self.env['res.city'].browse(vals.get('warehouse_dest_id')).name or carrier.city_id.id
                    price = str(vals.get('price_kg') or carrier.fixed_price)
                    name = '%s -> %s $ %s' % (warehouse_id, warehouse_dest_id, price)
                    carrier.write({'name': name})
        return super(DeliveryCarrier, self).write(vals)
