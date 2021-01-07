# -*- coding: utf-8 -*-
# from odoo import http


# class WebsiteSlidesExtender(http.Controller):
#     @http.route('/website_slides_extender/website_slides_extender/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_slides_extender/website_slides_extender/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_slides_extender.listing', {
#             'root': '/website_slides_extender/website_slides_extender',
#             'objects': http.request.env['website_slides_extender.website_slides_extender'].search([]),
#         })

#     @http.route('/website_slides_extender/website_slides_extender/objects/<model("website_slides_extender.website_slides_extender"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_slides_extender.object', {
#             'object': obj
#         })
