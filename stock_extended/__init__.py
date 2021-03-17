# -*- coding: utf-8 -*-

from . import controllers
from . import models
from . import wizard

from odoo.api import Environment, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    vals = {
        'group_stock_production_lot': True, 
        'group_stock_multi_locations': True,
    }
    env['res.config.settings'].create(vals).set_values()
    env.ref('stock_extended.report_delivery_guide').create_action()
