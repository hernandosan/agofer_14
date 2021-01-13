# -*- coding: utf-8 -*-

from . import controllers
from . import models
from . import wizard

from odoo.api import Environment, SUPERUSER_ID

def post_init_hook(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    vals = {
        'lock_confirmed_po': True,
        'group_product_variant': True,
    }
    env['res.config.settings'].create(vals).set_values()
