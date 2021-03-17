# -*- coding: utf-8 -*-
{
    'name': "HR Branch Agofer",

    'summary': "Allow define company branch for employee process",

    'description': "Allow define company branch for employee process",

    'author': "Agofer",
    'contributors': ['Juan Arcos jparcos@agofer.com.co'],
    'website': "https://www.agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '14.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_branch'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hr_branch_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
