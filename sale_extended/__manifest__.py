# -*- coding: utf-8 -*-
{
    'name': "Sales Agofer",

    'summary': "From quotations to invoices",

    'description': "From quotations to invoices",

    'author': "Agofer",
    'contributors': ['Juan Pablo Arcos jparcos@agofer.com.co'],
    'website': "https://agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/Sales',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': [
        'sale_stock', 
        'account_credit_control_extended'
    ],

    # always loaded
    'data': [
        'security/ir_rule_security.xml',
        'security/res_group_security.xml',
        'security/ir.model.access.csv',
        'data/account_incoterms_data.xml',
        'data/ir_cron_data.xml',
        'views/account_payment_view.xml',
        'views/crm_team_view.xml',
        'views/product_pricelist_view.xml',
        'views/product_template_view.xml',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
