# -*- coding: utf-8 -*-
# from odoo import http


# class AgnesAcademy(http.Controller):
#     @http.route('/agnes_academy/agnes_academy', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/agnes_academy/agnes_academy/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('agnes_academy.listing', {
#             'root': '/agnes_academy/agnes_academy',
#             'objects': http.request.env['agnes_academy.agnes_academy'].search([]),
#         })

#     @http.route('/agnes_academy/agnes_academy/objects/<model("agnes_academy.agnes_academy"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('agnes_academy.object', {
#             'object': obj
#         })

