from odoo import models, fields

class ResBankCustom(models.Model):
    _name = 'res.bank.custom'
    _inherit = 'res.bank'

    # Add custom fields or methods here
    custom_field = fields.Char(string='Custom Field')
