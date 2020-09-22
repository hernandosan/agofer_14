# -*- coding: utf-8 -*-
# from odoo import http


# class HelpdeskMgmtExtended(http.Controller):
#     @http.route('/helpdesk_mgmt_extended/helpdesk_mgmt_extended/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/helpdesk_mgmt_extended/helpdesk_mgmt_extended/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('helpdesk_mgmt_extended.listing', {
#             'root': '/helpdesk_mgmt_extended/helpdesk_mgmt_extended',
#             'objects': http.request.env['helpdesk_mgmt_extended.helpdesk_mgmt_extended'].search([]),
#         })

#     @http.route('/helpdesk_mgmt_extended/helpdesk_mgmt_extended/objects/<model("helpdesk_mgmt_extended.helpdesk_mgmt_extended"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('helpdesk_mgmt_extended.object', {
#             'object': obj
#         })
