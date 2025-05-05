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
    # day 2
    partner_id = fields.Many2one(
        'res.partner',
        string='Instructor',
    )
        # domain=[('is_instructor', '=', True)]
    course_id = fields.Many2one(
        'course.course',
        string='Course',
        required=True,
    )
        # domain="[('is_publish', '=', True),('state', 'in', ['in_progress', 'done'])]"
