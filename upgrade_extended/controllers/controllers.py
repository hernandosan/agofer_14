# -*- coding: utf-8 -*-
# from odoo import http


# class UpgradeExtended(http.Controller):
#     @http.route('/upgrade_extended/upgrade_extended/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/upgrade_extended/upgrade_extended/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('upgrade_extended.listing', {
#             'root': '/upgrade_extended/upgrade_extended',
#             'objects': http.request.env['upgrade_extended.upgrade_extended'].search([]),
#         })

#     @http.route('/upgrade_extended/upgrade_extended/objects/<model("upgrade_extended.upgrade_extended"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('upgrade_extended.object', {
#             'object': obj
#         })
