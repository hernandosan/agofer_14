from odoo import fields, models, api, _


class DeliveryRate(models.Model):
    _name = 'delivery.rate'
    _description = 'Delivery Rate'

    company_id = fields.Many2one('res.company', 'Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    city_id = fields.Many2one('res.city', 'Source Location', required=True)
    city_dest_id = fields.Many2one('res.city', 'Destination Location', required=True)
    name = fields.Char('Title')
    rate_lines_ids = fields.One2many('delivery.rate.line', 'rate_id', 'Values')
    rate_type = fields.Selection([('urban', 'Urban'), ('national', 'National')], 'Delivery Type', required=True)
    price_kg = fields.Monetary('Price by (Kg)')
    product_id = fields.Many2one('product.product', 'Product', required=True)
    tolerance = fields.Float('Tolerance (%)', help='Tolerance allowed in price.')
    notes = fields.Text('Terms and Conditions')

    def name_get(self):
        result = []
        for record in self:
            rec_name = "%s - %s (%s)" % (
                record.city_id.name, record.city_dest_id.name, _((record.rate_type).capitalize()))
            result.append((record.id, rec_name))
        return result


class DeliveryRateLine(models.Model):
    _name = 'delivery.rate.line'
    _description = 'Delivery Rate Line'

    company_id = fields.Many2one('res.company', 'Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    rate_id = fields.Many2one('delivery.rate', 'Rate')
    name = fields.Monetary('Value')
