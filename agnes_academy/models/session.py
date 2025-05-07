import logging
from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

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
    attendee_count = fields.Integer(
        string='Attendee Count',
        compute='_compute_attendee_count',
        store=True
    )
    seat_occupied = fields.Float(
        string='Seat Occupancy',
        compute='_compute_seat_occupied',
        store=True
    )

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done')
        ],
        string='Status', default='draft', tracking=True
    )

    @api.depends('attendee_ids')
    def _compute_attendee_count(self):
        for session in self:
            session.attendee_count = len(session.attendee_ids)

    @api.depends('attendee_ids', 'seat_total')
    def _compute_seat_occupied(self):
        for session in self:
            if session.seat_total > 0:
                session.seat_occupied = (len(session.attendee_ids) / session.seat_total) * 100
            else:
                session.seat_occupied = 0

    @api.onchange('seat_total')
    def onchange_seat_total(self):
        if self.seat_total and self.seat_total < 0:
            raise UserError('Number of seats most not negative!')

    @api.onchange('seat_total')
    def onchange_seat_total_check_attendee(self):
        if self.seat_total < len(self.attendee_ids):
            raise UserError('Unable to set Number of Seats less than registered Attendees')

    @api.onchange('attendee_ids')
    def onchange_attendee_ids(self):
        if self.attendee_ids and len(self.attendee_ids) > self.seat_total:
            # TODO: Find a way to reset attendee_ids if Onchange validation happened.
            self.attendee_ids = self._origin.attendee_ids
            raise UserError('Unable add more Attendee. There is not available seat!')
        # trial reset change, failed.
        # try:
        #     # risky logic that may raise UserError
        #     if self.attendee_ids and len(self.attendee_ids) > self.seat_total:
        #         raise UserError("Invalid selection!")
        # except UserError as e:
        #     # reset changes to discard
        #     self.attendee_ids = self._origin.attendee_ids
        #     # Optionally re-raise or just show a warning
        #     raise e

    @api.constrains('partner_id', 'attendee_ids')
    def _check_partner_attendance(self):
        for rec in self:
            if rec.partner_id and rec.partner_id in rec.attendee_ids:
                raise UserError('Instructor cannot be Attendee')

    def action_confirm(self):
        for session in self:
            if session.state != 'draft':
                raise UserError("Only draft sessions can be confirmed.")
            session.state = 'confirmed'
