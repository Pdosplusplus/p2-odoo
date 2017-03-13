# -*- coding: utf-8 -*-
from odoo import http

# class Dailyac(http.Controller):
#     @http.route('/dailyac/dailyac/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dailyac/dailyac/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dailyac.listing', {
#             'root': '/dailyac/dailyac',
#             'objects': http.request.env['dailyac.dailyac'].search([]),
#         })

#     @http.route('/dailyac/dailyac/objects/<model("dailyac.dailyac"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dailyac.object', {
#             'object': obj
#         })