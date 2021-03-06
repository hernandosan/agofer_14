# -*- coding: utf-8 -*-
{
    'name': "Upgrade Agofer",

    'summary': "Upgrade Agofer",

    'description': "Upgrade Agofer",

    'author': "Agofer",
    'contributors': [
        'Juan Pablo Arcos jparcos@agofer.com.co',
        'Reyes Hernando Santana rhsantana@agofer.com.co',
    ],
    'website': "https://agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.1',

    # any module necessary for this one to work correctly
    'depends': [
        # Avancys
        'account_avancys',
        'electronic_invoice_dian',
        'hr_avancys',
        # OCA
        'account_asset_management',
        'account_tax_balance',
        'account_financial_report',
        'auth_oauth_multi_token',
        # Odoo
        'auth_oauth',
        'base_address_city',
        'board',
        'crm',
        'hr_contract',
        'hr_gamification',
        'hr_recruitment',
        'mass_mailing',
        'l10n_co',
        'purchase_requisition',
        # Extended
        'account_extended',
        # 'base_user_role_extended',
        'helpdesk_mgmt_extended',
        'hr_extended',
        'mrp_extended',
        'sale_extended',
        'stock_account_extended',
        'stock_extended',
        'purchase_extended',
        'website_slides_extended',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    # 'pre_init_hook': 'pre_init_hook',
    #
    # 'post_init_hook': 'post_init_hook',
}
