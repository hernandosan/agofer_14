# -*- coding: utf-8 -*-
# from odoo import http


# class HrBranchExtended(http.Controller):
#     @http.route('/hr_branch_extended/hr_branch_extended/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_branch_extended/hr_branch_extended/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_branch_extended.listing', {
#             'root': '/hr_branch_extended/hr_branch_extended',
#             'objects': http.request.env['hr_branch_extended.hr_branch_extended'].search([]),
#         })

#     @http.route('/hr_branch_extended/hr_branch_extended/objects/<model("hr_branch_extended.hr_branch_extended"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_branch_extended.object', {
#             'object': obj
#         })
