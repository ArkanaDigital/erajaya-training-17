# -*- coding: utf-8 -*-
# from odoo import http


# class AndiAcademy(http.Controller):
#     @http.route('/andi_academy/andi_academy', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/andi_academy/andi_academy/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('andi_academy.listing', {
#             'root': '/andi_academy/andi_academy',
#             'objects': http.request.env['andi_academy.andi_academy'].search([]),
#         })

#     @http.route('/andi_academy/andi_academy/objects/<model("andi_academy.andi_academy"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('andi_academy.object', {
#             'object': obj
#         })

