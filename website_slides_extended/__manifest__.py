# -*- coding: utf-8 -*-
{
    'name': "eLearning Agofer",

    'summary': "Manage and publish an eLearning platform",

    'description': "Manage and publish an eLearning platform",

    'author': "Agofer",
    'contributors': ['Reyes Hernando Santana rhsantana@agofer.com.co'],
    'website': "https://www.agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website/eLearning',
    'version': '14.1',

    # any module necessary for this one to work correctly
    'depends': [
        # 'website_slides',
        'website_slides_survey',
        ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/slide_channel_tags.xml',
        'data/slide_channel_accounting.xml',
        'data/slide_channel_general.xml',
        'data/slide_channel_inventory.xml',
        'data/slide_channel_production.xml',
        'data/slide_channel_purchases.xml',
        'data/slide_channel_sales.xml',
        'data/slide_channel_wallet.xml',
    ],
}
