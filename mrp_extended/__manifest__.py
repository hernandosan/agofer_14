# -*- coding: utf-8 -*-
{
    'name': "Manufacturing Agofer",

    'summary': "Manufacturing Orders & BOMs",

    'description': "Manufacturing Orders & BOMs",

    'author': "Agofer S.A.",
    'contributors': ['Juan Pablo Arcos jparcos@agofer.com.co'],
    'website': "http://www.agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing/Manufacturing',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['mrp_account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/account_journal.xml',
        'views/mrp_workcenter_view.xml',
        'views/mrp_production_view.xml',
        'views/templates.xml',
        'wizard/mrp_product_produce_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
