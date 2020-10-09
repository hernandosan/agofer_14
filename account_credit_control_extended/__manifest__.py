# -*- coding: utf-8 -*-
{
    'name': "Account Credit Control Agofer",

    'summary': "Account Credit Control",

    'description': "Account Credit Control",

    'author': "Agofer S.A.",
    'contributors': ['Juan Pablo Arcos jparcos@agofer.com.co'],
    'website': "http://www.agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Finance',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['account_credit_control'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/mail_template_data.xml',
        'data/ir_cron_data.xml',
        'views/res_partner_view.xml',
        'views/account_payment_term_view.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
