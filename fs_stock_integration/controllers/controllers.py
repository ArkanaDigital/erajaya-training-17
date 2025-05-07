# -*- coding: utf-8 -*-
# from odoo import http


# class FsStockIntegration(http.Controller):
#     @http.route('/fs_stock_integration/fs_stock_integration', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fs_stock_integration/fs_stock_integration/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('fs_stock_integration.listing', {
#             'root': '/fs_stock_integration/fs_stock_integration',
#             'objects': http.request.env['fs_stock_integration.fs_stock_integration'].search([]),
#         })

#     @http.route('/fs_stock_integration/fs_stock_integration/objects/<model("fs_stock_integration.fs_stock_integration"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fs_stock_integration.object', {
#             'object': obj
#         })

