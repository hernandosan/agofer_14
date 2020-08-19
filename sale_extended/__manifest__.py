# -*- coding: utf-8 -*-
{
    'name': "Sales Agofer",

    'summary': "From quotations to invoices",

    'description': "From quotations to invoices",

    'author': "Agofer S.A.",
    'contributors': ['Juan Pablo Arcos jparcos@agofer.com.co'],
    'website': "http://www.agofer.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/Sales',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['sale_management'],

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
}
