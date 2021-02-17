# -*- coding: utf-8 -*-
{
    'name': "Scan Documents Agofer",

    'summary': "Attach files to different documents",

    'description': "Attach files to different documents",

    'author': "Agofer",
    'contributors': ['Reyes Hernando Santana rhsantana@agofer.com.co'],
    'website': "https://agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'portal'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
    ],
}
