# -*- coding: utf-8 -*-
{
    'name': "Account Credit Control Agofer",

    'summary': "Account Credit Control",

    'description': "Account Credit Control",

    'author': "Agofer",
    'contributors': [
        'Juan Pablo Arcos jparcos@agofer.com.co',
        'Reyes Santana rhsantana@agofer.com.co',
    ],
    'website': "https://agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Finance',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': [
        'account_credit_control', 
        'contacts',
        'sale'
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/credit_document_type_data.xml',
        'data/ir_cron_data.xml',
        'data/mail_template_data.xml',
        'views/account_payment_term_view.xml',
        'views/credit_document_type_view.xml',
        'views/credit_document_view.xml',
        'views/res_partner_view.xml',
        'wizard/credit_interest_wizard_template.xml',
        'wizard/credit_interest_wizard_view.xml',
        'wizard/credit_wallet.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
