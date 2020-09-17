# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sale_delay = fields.Float(default=3)
    upload_delay = fields.Float('Customer Upload Time', default=2)
    delivery_delay = fields.Float('Customer Delivery Time', default=1)
