# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class fs_stock_integration(models.Model):
#     _name = 'fs_stock_integration.fs_stock_integration'
#     _description = 'fs_stock_integration.fs_stock_integration'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

