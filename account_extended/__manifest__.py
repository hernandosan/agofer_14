# -*- coding: utf-8 -*-
{
    'name': "Invoicing Agofer",

    'summary': "Invoices & Payments",

    'description': "Invoices & Payments",

    'author': "Agofer S.A.",
    'contributors': ['Juan Pablo Arcos jparcos@agofer.com.co'],
    'website': "http://www.agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting/Accounting',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/res_group_security.xml',
        'views/account_payment_view.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
