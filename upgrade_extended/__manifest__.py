# -*- coding: utf-8 -*-
{
    'name': "Upgrade Agofer",

    'summary': "Upgrade Agofer",

    'description': "Upgrade Agofer",

    'author': "Agofer S.A.S.",
    'contributors': ['Juan Pablo Arcos jparcos@agofer.com.co'],
    'website': "http://www.agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.1',

    # any module necessary for this one to work correctly
    'depends': [
        # Odoo 
        'auth_oauth',
        'base_address_city',
        'base_address_extended',
        'hr_contract',
        'hr_recruitment',
        'l10n_co',
        'web',
        # OCA 
        'account_asset_management',
        'account_payment_order',
        # Extended
        'account_extended',
        'helpdesk_mgmt_extended',
        'hr_extended',
        # 'mrp_extended',
        'sale_extended',
        'stock_account_extended',
        'stock_extended',
        'purchase_extended',
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

    # 'post_init_hook': 'post_init_hook',
}
