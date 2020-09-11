# -*- coding: utf-8 -*-
# from odoo import http


# class AccountCreditControlExtended(http.Controller):
#     @http.route('/account_credit_control_extended/account_credit_control_extended/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_credit_control_extended/account_credit_control_extended/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_credit_control_extended.listing', {
#             'root': '/account_credit_control_extended/account_credit_control_extended',
#             'objects': http.request.env['account_credit_control_extended.account_credit_control_extended'].search([]),
#         })

#     @http.route('/account_credit_control_extended/account_credit_control_extended/objects/<model("account_credit_control_extended.account_credit_control_extended"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_credit_control_extended.object', {
#             'object': obj
#         })
