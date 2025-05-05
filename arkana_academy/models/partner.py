from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_instructor = fields.Boolean(string="Is Instructor")
    course_session_ids = fields.One2many('course.session', 'partner_id', string='Course Session')

    