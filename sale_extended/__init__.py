# -*- coding: utf-8 -*-

from . import controllers
from . import models

from odoo.api import Environment, SUPERUSER_ID

def post_init_hook(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    vals = {
        'group_uom': True, 
        'group_discount_per_so_line': True, 
        'group_product_pricelist': True, 
        'product_pricelist_setting': 'advanced', 
        'group_sale_delivery_address': True, 
        'group_auto_done_setting': True, 
        'group_display_incoterm': True, 
    }
    env['res.config.settings'].create(vals).set_values()
