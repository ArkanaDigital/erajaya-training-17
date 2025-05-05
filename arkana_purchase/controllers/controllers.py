# -*- coding: utf-8 -*-
# from odoo import http


# class ArkanaPurchase(http.Controller):
#     @http.route('/arkana_purchase/arkana_purchase', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/arkana_purchase/arkana_purchase/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('arkana_purchase.listing', {
#             'root': '/arkana_purchase/arkana_purchase',
#             'objects': http.request.env['arkana_purchase.arkana_purchase'].search([]),
#         })

#     @http.route('/arkana_purchase/arkana_purchase/objects/<model("arkana_purchase.arkana_purchase"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('arkana_purchase.object', {
#             'object': obj
#         })

