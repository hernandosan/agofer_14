# -*- coding: utf-8 -*-
# from odoo import http


# class MrpExtended(http.Controller):
#     @http.route('/mrp_extended/mrp_extended/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrp_extended/mrp_extended/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrp_extended.listing', {
#             'root': '/mrp_extended/mrp_extended',
#             'objects': http.request.env['mrp_extended.mrp_extended'].search([]),
#         })

#     @http.route('/mrp_extended/mrp_extended/objects/<model("mrp_extended.mrp_extended"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrp_extended.object', {
#             'object': obj
#         })
