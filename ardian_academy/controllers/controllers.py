# -*- coding: utf-8 -*-
# from odoo import http


# class ArdianAcademy(http.Controller):
#     @http.route('/ardian_academy/ardian_academy', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ardian_academy/ardian_academy/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ardian_academy.listing', {
#             'root': '/ardian_academy/ardian_academy',
#             'objects': http.request.env['ardian_academy.ardian_academy'].search([]),
#         })

#     @http.route('/ardian_academy/ardian_academy/objects/<model("ardian_academy.ardian_academy"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ardian_academy.object', {
#             'object': obj
#         })

