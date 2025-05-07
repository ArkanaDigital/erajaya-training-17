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

    @api.constrains('is_instructor')
    def _check_instructor(self):
        for record in self:
            # prevent setting is_instructor to True if is_company is False
            if len(record.course_session_ids) > 0:
                raise ValidationError(
                    'Unable to set Is Instructor to False if session reference exists.'
                )
            # unlink all instructure from session
            # if record.course_session_ids:
            #     record.course_session_ids.write({'partner_id': False})

    # def create(self, vals):
    #     for val in vals:
    #         if val.get('is_instructor') and not val.get('is_company'):
    #             raise ValidationError(_("A partner cannot be an instructor unless they are marked as a company."))
    #     return super(Partner, self).create(vals)
