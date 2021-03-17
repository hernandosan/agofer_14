# -*- coding: utf-8 -*-
# from odoo import http


# class ExternalLayoutExtended(http.Controller):
#     @http.route('/external_layout_extended/external_layout_extended/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/external_layout_extended/external_layout_extended/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('external_layout_extended.listing', {
#             'root': '/external_layout_extended/external_layout_extended',
#             'objects': http.request.env['external_layout_extended.external_layout_extended'].search([]),
#         })

#     @http.route('/external_layout_extended/external_layout_extended/objects/<model("external_layout_extended.external_layout_extended"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('external_layout_extended.object', {
#             'object': obj
#         })
