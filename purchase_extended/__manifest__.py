# -*- coding: utf-8 -*-
{
    'name': "Purchase Agofer",

    'summary': "Purchase orders, tenders and agreements",

    'description': "Purchase orders, tenders and agreements",

    'author': "Agofer",
    'contributors': ['Juan Pablo Arcos jparcos@agofer.com.co'],
    'website': "https://agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Operations/Purchase',
    'version': '14.1',

    # any module necessary for this one to work correctly
    'depends': ['stock_extended'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/res_group_security.xml',
        'data/ir_sequence_data.xml',
        'data/product_template_data.xml',
        'wizard/stock_picking_wizard_view.xml',
        'views/account_move_view.xml',
        'views/delivery_carrier_view.xml',
        'views/product_supplierinfo_view.xml',
        'views/product_template_view.xml',
        'views/purchase_import_view.xml',
        'views/purchase_order_view.xml',
        'views/stock_landed_cost_view.xml',
        'views/stock_move_view.xml',
        'views/stock_picking_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
