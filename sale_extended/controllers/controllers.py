# -*- coding: utf-8 -*-
# from odoo import http


# class SaleExtended(http.Controller):
#     @http.route('/sale_extended/sale_extended/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_extended/sale_extended/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_extended.listing', {
#             'root': '/sale_extended/sale_extended',
#             'objects': http.request.env['sale_extended.sale_extended'].search([]),
#         })

#     @http.route('/sale_extended/sale_extended/objects/<model("sale_extended.sale_extended"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_extended.object', {
#             'object': obj
#         })
