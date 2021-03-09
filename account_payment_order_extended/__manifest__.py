# -*- coding: utf-8 -*-
{
    'name': "Account Payment Order Agofer",

    'summary': "Account Payment Order Agofer",

    'description': "Account Payment Order Agofer",

    'author': "Agofer",
    'website': "https://www.agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Banking Addons',
    'version': '14.1',

    # any module necessary for this one to work correctly
    'depends': ['account_payment_order'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/account_payment_method.xml',
        'reports/account_payment_order_report.xml',
        'views/account_payment_order_view.xml',
        'views/res_bank_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
