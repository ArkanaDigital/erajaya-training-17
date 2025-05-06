from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Partner(models.Model):
    _inherit = 'res.partner'

    is_instructor = fields.Boolean(
        string="Is Instructor"
    )
    course_session_ids = fields.One2many(
        'course.session',
        'partner_id',
        string='Course Session'
    )

    # def create(self, vals):
    #     for val in vals:
    #         if val.get('is_instructor') and not val.get('is_company'):
    #             raise ValidationError(_("A partner cannot be an instructor unless they are marked as a company."))
    #     return super(Partner, self).create(vals)
