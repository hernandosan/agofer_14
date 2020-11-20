# -*- coding: utf-8 -*-
{
    'name': "Inventory Agofer",

    'summary': "Manage your stock and logistics activities",

    'description': "Manage your stock and logistics activities",

    'author': "Agofer S.A.",
    'contributors': ['Juan Pablo Arcos jparcos@agofer.com.co'],
    'website': "http://www.agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Operations/Inventory',
    'version': '14.1',

    # any module necessary for this one to work correctly
    'depends': [
        'delivery',
        'stock_account_extended',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/res_partner_category_data.xml',
        'views/account_move_view.xml',
        'views/delivery_carrier_view.xml',
        'views/delivery_guide_view.xml',
        'views/product_template_view.xml',
        'views/stock_landed_cost_view.xml',
        'views/stock_picking_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}