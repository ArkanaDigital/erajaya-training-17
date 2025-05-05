from odoo import fields, models, api, _
from odoo.exceptions import UserError

class SesstionAddAttendeeWizard(models.TransientModel):
    _name = 'session.add.attendee.wizard'
    _description = 'Session Add Attendee Wizard'

    @api.model
    def default_get(self, fields):
        res = super(SesstionAddAttendeeWizard, self).default_get(fields)
        if self.env.context.get('active_model') == 'course.session' and self.env.context.get('active_id'):
            res['session_id'] = self.env.context['active_id']
        return res

    session_id = fields.Many2one('course.session', string='Session')
    instructor_id = fields.Many2one('res.partner', string='Instructor', related='session_id.partner_id')
    attendee_ids = fields.Many2many('res.partner', string='Attendees')

    def action_add_attendees(self):
        self.ensure_one()
        if not self.session_id:
            raise UserError(_('Please select a session.'))
        self.session_id.attendee_ids |= self.attendee_ids
