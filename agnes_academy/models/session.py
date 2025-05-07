import logging
from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class CourseSession(models.Model):
    _name = 'course.session'
    _description = 'Course Session'

    # day 1
    name = fields.Char(string='Sesssion', default=False, tracking=True)
    start_date = fields.Date(string='Start Date', default=fields.Date.today, tracking=True)
    duration = fields.Float(string='Duration', tracking=True)
    seat_total = fields.Integer(string='Number of Seats', default=10, tracking=True)

    partner_id = fields.Many2one(
        'res.partner',
        string='Instructor',
        domain="[('is_instructor', '=', True)]",
    )
    # '|', ('is_instructor', '=', True),('vat', 'ilike', 'ABC')
    course_id = fields.Many2one(
        'course.course',
        string='Course',
        required=True,
    )
    attendee_ids = fields.Many2many(
        'res.partner',
        string='Attendees'
    )

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done')
        ],
        string='Status', default='draft', tracking=True
    )

    def action_confirm(self):
        for session in self:
            if session.state != 'draft':
                raise UserError("Only draft sessions can be confirmed.")
            session.state = 'confirmed'
