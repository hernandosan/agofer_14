# -*- coding: utf-8 -*-
{
    'name': "User Roles Agofer",

    'summary': "User Roles Agofer",

    'description': "User Roles Agofer",

    'author': "Agofer",
    'website': "https://agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '14.1',

    # any module necessary for this one to work correctly
    'depends': [
        # Odoo
        'hr_recruitment',
        'purchase',
        'survey',
        # OCA
        'account_credit_control',
        'base_user_role',
        'helpdesk_mgmt',
        # Agofer
        'account_extended',
        'mrp_extended',
        'sale_extended',
        'stock_extended',
        # Avancys
        'account_avancys',
        'electronic_invoice_dian',
        'hr_avancys',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'data/res_users_role_treasury.xml',
        'data/res_users_role_account.xml',
        'data/res_users_role_admin.xml',
        'data/res_users_role_credit.xml',
        'data/res_users_role_hr.xml',
        'data/res_users_role_purchase.xml',
        'data/res_users_role_sale.xml',
        'data/res_users_role_stock.xml',
        'views/res_users_role_view.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
