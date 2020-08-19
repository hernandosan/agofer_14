# -*- coding: utf-8 -*-
# from odoo import http


# class StockAccountExtended(http.Controller):
#     @http.route('/stock_account_extended/stock_account_extended/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_account_extended/stock_account_extended/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_account_extended.listing', {
#             'root': '/stock_account_extended/stock_account_extended',
#             'objects': http.request.env['stock_account_extended.stock_account_extended'].search([]),
#         })

#     @http.route('/stock_account_extended/stock_account_extended/objects/<model("stock_account_extended.stock_account_extended"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_account_extended.object', {
#             'object': obj
#         })
