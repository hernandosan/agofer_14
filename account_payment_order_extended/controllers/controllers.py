# -*- coding: utf-8 -*-
# from odoo import http


# class AccountPaymentOrderExtended(http.Controller):
#     @http.route('/account_payment_order_extended/account_payment_order_extended/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_payment_order_extended/account_payment_order_extended/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_payment_order_extended.listing', {
#             'root': '/account_payment_order_extended/account_payment_order_extended',
#             'objects': http.request.env['account_payment_order_extended.account_payment_order_extended'].search([]),
#         })

#     @http.route('/account_payment_order_extended/account_payment_order_extended/objects/<model("account_payment_order_extended.account_payment_order_extended"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_payment_order_extended.object', {
#             'object': obj
#         })
