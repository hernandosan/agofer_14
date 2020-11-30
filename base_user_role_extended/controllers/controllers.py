# -*- coding: utf-8 -*-
# from odoo import http


# class BaseUserRoleExtended(http.Controller):
#     @http.route('/base_user_role_extended/base_user_role_extended/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/base_user_role_extended/base_user_role_extended/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('base_user_role_extended.listing', {
#             'root': '/base_user_role_extended/base_user_role_extended',
#             'objects': http.request.env['base_user_role_extended.base_user_role_extended'].search([]),
#         })

#     @http.route('/base_user_role_extended/base_user_role_extended/objects/<model("base_user_role_extended.base_user_role_extended"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('base_user_role_extended.object', {
#             'object': obj
#         })
