# -*- coding: utf-8 -*-
{
    'name': "HR Agofer",

    'summary': "HR Employee",

    'description': "HR Employee",

    'author': "Agofer",
    'contributors': [
        'Juan Arcos jparcos@agofer.com.co',
        'Reyes Santana rhsantana@agofer.com.co'
        ],
    'website': "https://agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources/Employees',
    'version': '14.0',

    # any module necessary for this one to work correctly
    'depends': ['hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'data/mail_template_data.xml',
        'views/hr_doc_type_view.xml',
        'views/hr_document_view.xml',
        'views/hr_employee_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
