# -*- coding: utf-8 -*-
# from odoo import http


# class StockExtended(http.Controller):
#     @http.route('/stock_extended/stock_extended/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_extended/stock_extended/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_extended.listing', {
#             'root': '/stock_extended/stock_extended',
#             'objects': http.request.env['stock_extended.stock_extended'].search([]),
#         })

#     @http.route('/stock_extended/stock_extended/objects/<model("stock_extended.stock_extended"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_extended.object', {
#             'object': obj
#         })
