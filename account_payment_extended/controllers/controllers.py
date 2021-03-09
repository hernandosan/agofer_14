# -*- coding: utf-8 -*-
# from odoo import http


# class AccountPaymentExtended(http.Controller):
#     @http.route('/account_payment_extended/account_payment_extended/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_payment_extended/account_payment_extended/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_payment_extended.listing', {
#             'root': '/account_payment_extended/account_payment_extended',
#             'objects': http.request.env['account_payment_extended.account_payment_extended'].search([]),
#         })

#     @http.route('/account_payment_extended/account_payment_extended/objects/<model("account_payment_extended.account_payment_extended"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_payment_extended.object', {
#             'object': obj
#         })
