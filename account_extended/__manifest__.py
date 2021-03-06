# -*- coding: utf-8 -*-
{
    'name': "Invoicing Agofer",

    'summary': "Invoices & Payments",

    'description': "Invoices & Payments",

    'author': "Agofer",
    'contributors': ['Juan Pablo Arcos jparcos@agofer.com.co'],
    'website': "https://agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting/Accounting',
    'version': '14.1',

    # any module necessary for this one to work correctly
    'depends': [
        'account_asset_management',
        'account_menu',
        'sale_extended',
    ],

    # always loaded
    'data': [
        'security/res_group_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'reports/report_account_invoice.xml',
        'reports/report_account_move.xml',
        'reports/report_try.xml',
        'views/account_account_view.xml',
        'views/account_consignment_view.xml',
        'views/account_journal_view.xml',
        'views/account_move_line_view.xml',
        'views/account_move_view.xml',
        'views/account_payment_view.xml',
        'views/res_currency_rate_view.xml',
        'views/res_partner_view.xml',
        'wizard/account_consignment_wizard_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'post_init_hook': 'post_init_hook',
}
