# -*- coding: utf-8 -*-
{
    'name': "Payment Account Agofer",

    'summary': "Payment Account",

    'description': "Payment Account",

    'author': "Agofer",
    'website': "https://www.agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting/Accounting',
    'version': '14.1',

    # any module necessary for this one to work correctly
    'depends': [
        'account_payment',
        'hr_branch_extended',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/account_payment_view.xml',
        'views/hr_branch_view.xml',
        'views/payment_line_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
