# -*- coding: utf-8 -*-
{
    'name': "Helpdesk Management Agofer",

    'summary': "Helpdesk",

    'description': "Helpdesk",

    'author': "Agofer S.A.",
    'contributors': ['Reyes Santana rhsantana@agofer.com.co'],
    'website': "http://www.agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'After-Sales',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['helpdesk_mgmt'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/helpdesk_ticket_stage_data.xml',
        'data/helpdesk_ticket_type_data.xml',
        # 'data/helpdesk_ticket_team_data.xml',
        'views/helpdesk_sla_view.xml',
        'views/helpdesk_ticket_category_view.xml',
        'views/helpdesk_ticket_team_view.xml',
        'views/helpdesk_ticket_type_view.xml',
        # 'views/helpdesk_ticket_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
