# -*- coding: utf-8 -*-
{
    'name': "Purchase Agofer",

    'summary': "Purchase orders, tenders and agreements",

    'description': "Purchase orders, tenders and agreements",

    'author': "Agofer S.A.",
    'contributors': ['Juan Pablo Arcos jparcos@agofer.com.co'],
    'website': "http://www.agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Operations/Purchase',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase_stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'views/purchase_import_view.xml',
        'views/purchase_order_view.xml',
        'views/product_template_view.xml',
        # 'views/stock_move_view.xml',
        'views/account_move_view.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}