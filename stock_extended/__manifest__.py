# -*- coding: utf-8 -*-
{
    'name': "Inventory Agofer",

    'summary': "Manage your stock and logistics activities",

    'description': "Manage your stock and logistics activities",

    'author': "Agofer",
    'contributors': ['Juan Pablo Arcos jparcos@agofer.com.co'],
    'website': "https://agofer.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Operations/Inventory',
    'version': '14.1',

    # any module necessary for this one to work correctly
    'depends': [
        'account_extended',
        'delivery',
        'sale_extended',
        'stock_account_extended',
        'base_address_city',
    ],

    # always loaded
    'data': [
        'security/res_groups_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/res_partner_category_data.xml',
        'reports/report_delivery_guide.xml',
        'reports/report_stock_picking.xml',
        'wizard/sale_advance_payment_inv_view.xml',
        'wizard/update_delivery_guide_view.xml',
        # 'views/account_move_view.xml',
        'views/delivery_carrier_view.xml',
        # 'views/delivery_guide_move_view.xml',
        'views/delivery_guide_view.xml',
        'views/delivery_invoice_view.xml',
        'views/delivery_rate_view.xml',
        'views/ir_ui_menu_view.xml',
        'views/product_product_view.xml',
        'views/product_template_view.xml',
        'views/res_partner_view.xml',
        # 'views/stock_landed_cost_view.xml',
        'views/stock_move_view.xml',
        'views/stock_picking_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'post_init_hook': 'post_init_hook',
}
