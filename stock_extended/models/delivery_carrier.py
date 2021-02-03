# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    name = fields.Char(required=True)
    carrier_type = fields.Selection([('stock','Stock'), ('purchase','Purchase')], 'Delivery Type', default='stock')
    partner_id = fields.Many2one('res.partner', 'Carrier')
    city_id = fields.Many2one('res.city', 'Source Location')
    city_dest_id = fields.Many2one('res.city', 'Destination Location')
    price_kg = fields.Float('Price (Kg)')
    tolerance = fields.Float('Tolerance (%)', help='Tolerance allowed in price.')
    notes = fields.Text('Terms and Conditions')

