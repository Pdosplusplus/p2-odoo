# -*- coding: utf-8 -*-
from odoo import http

# class Agilis(http.Controller):
#     @http.route('/agilis/agilis/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/agilis/agilis/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('agilis.listing', {
#             'root': '/agilis/agilis',
#             'objects': http.request.env['agilis.agilis'].search([]),
#         })

#     @http.route('/agilis/agilis/objects/<model("agilis.agilis"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('agilis.object', {
#             'object': obj
#         })