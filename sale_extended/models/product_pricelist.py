# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    discount_maximum = fields.Float('Maximum percentage', default=10, help='Maximum discount allowed in the order')
    discount_freight = fields.Float('Freight percentage', default=2, help='Maximum discount allowed when the customer collects')
