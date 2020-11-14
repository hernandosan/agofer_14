# -*- coding: utf-8 -*-
{
    'name': "WMS Accounting Agofer",

    'summary': "Inventory, Logistic, Valuation, Accounting",

    'description': "Inventory, Logistic, Valuation, Accounting",

    'author': "Agofer S.A.",
    'contributors': ['Juan Pablo Arcos jparcos@agofer.com.co'],
    'website': "http://www.agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Hidden',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': [
        'stock_account',
        'sale_purchase_stock',
        'stock_landed_costs',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order_view.xml',
        'views/stock_kardex_view.xml',
        'views/stock_landed_cost_view.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
