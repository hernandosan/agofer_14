# -*- coding: utf-8 -*-
{
    'name': "website_slides_extended",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['website_slides'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/slide_channel_tags.xml',
        'data/slide_channel_accounting.xml',
        'data/slide_channel_general.xml',
        'data/slide_channel_inventory.xml',
        'data/slide_channel_production.xml',
        'data/slide_channel_purchases.xml',
        'data/slide_channel_sales.xml',
        'data/slide_channel_wallet.xml',
    ],
}
