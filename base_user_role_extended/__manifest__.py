# -*- coding: utf-8 -*-
{
    'name': "User Roles Agofer",

    'summary': "User Roles Agofer",

    'description': "User Roles Agofer",

    'author': "Agofer S.A.",
    'website': "http://www.agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '14.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base_user_role',
        'sales_team',
        'purchase'
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/res_users_role_data.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
