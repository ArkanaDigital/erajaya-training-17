import logging
from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class CourseSession(models.Model):
    _name = 'course.session'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Course Session'


    def get_ready_course_id(self):
        unselect_course_ids = []
        # course_ids = self.env['course.course'].search([])
        # session_ids = self.search([])
        # for course in course_ids:
        #     if course.name not in session_ids.mapped('name'):
        #         unselect_course_ids.append(course.id)
        # sql = """select """
        return [('id', 'in', unselect_course_ids)]

    def get_default_name(self):
        return 'Sesi per hari %s' % (str(fields.Date.today()))

    name = fields.Char(string='Sesssion', default=get_default_name, tracking=True)
    start_date = fields.Date(string='Start Date', default=fields.Date.today, tracking=True)
    duration = fields.Float(string='Duration', tracking=True)
    seat_total = fields.Integer(string='Number of Seats', default=10, tracking=True)
    # day 2
    partner_id = fields.Many2one(
        'res.partner',
        string='Instructor',
        domain=[('is_instructor', '=', True)]
    )
    course_id = fields.Many2one(
        'course.course',
        string='Course',
        required=True,
        domain="[('is_publish', '=', True),('state', 'in', ['in_progress', 'done'])]"
    )
    course_ids = fields.Many2many('course.course', string='Courses')
    # ready_course_id = fields.Many2one('course.course', domain=lambda self: self.get_ready_course_id())
    ready_course_id = fields.Many2one('course.course', domain=get_ready_course_id)
    attendee_ids = fields.Many2many('res.partner', string='Attendees')
    attendee_count = fields.Integer(
        string='Attendee Count',
        compute='_compute_attendee_count',
        store=True
    )
    seat_occupied = fields.Float(
        string='Seat Occupancy',
        compute='compute_seat_occupied',
        store=True
    )
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done')
        ],
        string='Status', default='draft', tracking=True
    )
    stage_id = fields.Many2one(
        'course.session.stage',
        string='Stage',
        group_expand='_read_group_stage_ids'
    )

    _sql_constraints = [('name_unique', 'UNIQUE(name)', 'Session name must be unique')]

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['course.session.stage'].search([])
        return stage_ids

    @api.depends('attendee_ids', 'seat_total')
    def compute_seat_occupied(self):
        for rec in self:
            if rec.attendee_ids and rec.seat_total:
                rec.seat_occupied = len(rec.attendee_ids.ids) / rec.seat_total * 100
            else:
                rec.seat_occupied = 0

    @api.depends('attendee_ids')
    def _compute_attendee_count(self):
        for rec in self:
            rec.attendee_count = len(rec.attendee_ids)

    @api.onchange('seat_total')
    def onchange_seat_total(self):
        if self.seat_total and self.seat_total < 0:
            raise UserError('Number of seats most not negative!')
        if self.seat_total < len(self.attendee_ids):
            raise UserError('Unable to set Number of Seats less than registered Attendees')

    @api.onchange('attendee_ids')
    def onchange_attendee_ids(self):
        if self.attendee_ids and len(self.attendee_ids) > self.seat_total:
            # TODO: Find a way to reset attendee_ids if Onchange validation happened.
            # self.attendee_ids = self._origin.attendee_ids
            raise UserError('Unable add more Attendee. There is not available seat!')

    @api.constrains('attendee_ids', 'seat_total')
    def check_attendee_to_seat(self):
        for rec in self:
            if rec.attendee_ids and rec.seat_total and len(rec.attendee_ids) > rec.seat_total:
                raise UserError('Attendee cannot more than available seat')

    @api.constrains('partner_id', 'attendee_ids')
    def _check_partner_attendance(self):
        for rec in self:
            if rec.partner_id and rec.partner_id in rec.attendee_ids:
                raise UserError('Instructor cannot be Attendee')

    @api.model
    def create(self, vals):
        if vals.get('state') == 'confirmed':
            vals['name'] = self.env['ir.sequence'].next_by_code('course.session') or '/'
        return super(CourseSession, self).create(vals)

    def write(self, vals):
        if 'state' in vals and vals['state'] == 'confirmed':
            vals['name'] = self.env['ir.sequence'].next_by_code('course.session') or '/'
        return super(CourseSession, self).write(vals)

    def copy(self, default=None):
        default = dict(default or {})
        default['name'] = ''
        return super(CourseSession, self).copy(default)

    def action_set_draft(self):
        if self.state not in (None, 'confirmed', 'done'):
            raise UserError('Unable to set to draft document that is not in confirmed or done state')
        self.write({'state': 'draft'})

    def action_set_confirmed(self):
        if self.state not in ('draft'):
            raise UserError('Unable to confirm document that is not in draft state')
        self.write({'state': 'confirmed'})

    def action_set_done(self):
        if self.state not in ('confirmed'):
            raise UserError('Unable to set to done docuumet that is not in confirmed state')
        self.write({'state': 'done'})

    def action_send_session_email(self):
        self.ensure_one()
        template = self.env.ref('arkana_academy.email_template_course_session')

        # For compositions
        ctx = {
            'default_model': 'course.session',
            'default_res_ids': self.ids,
            'default_use_template': bool(template),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'force_email': True,
        }

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def notify_upcoming_sessions(self):
        """
        Scheduled action to notify instructors about their upcoming sessions
        Checks for sessions starting tomorrow and sends email notification
        """
        tomorrow = fields.Date.today() + timedelta(days=1)
        upcoming_sessions = self.search([
            ('start_date', '=', tomorrow),
            ('state', '=', 'confirmed'),
            ('partner_id', '!=', False)
        ])

        # notify todo
        _logger.error("Course Session Datas: %s" % (upcoming_sessions.ids))

        email_template = self.env.ref('arkana_academy.email_template_course_session')
        # email_template = self.env.ref('arkana_academy.email_template_upcoming_reminder')

        for session in upcoming_sessions:
            # Prepare email values for instructor
            email_values = {
                'email_to': session.partner_id.email,
                'subject': f'Reminder: Tomorrow\'s Session - {session.name}',
                'body_html': f'''
                    <p>Dear {session.partner_id.name},</p>
                    <p>This is a reminder about your session tomorrow:</p>
                    <ul>
                        <li>Session: {session.name}</li>
                        <li>Course: {session.course_id.name}</li>
                        <li>Duration: {session.duration} Hours</li>
                        <li>Attendees: {session.attendee_count}</li>
                    </ul>
                    <p>Best regards,<br/>Course Management</p>
                '''
            }

            try:
                email_template.with_context(custom_layout=True).send_mail(
                    session.id,
                    email_values=email_values,
                    force_send=True
                )
            except Exception as e:
                _logger.error(f"Failed to send reminder for session {session.name}: {str(e)}")

    def get_session_info(self):
        self.ensure_one()
        # logic here
        return {
            'status_code': 200,
            'message': 'Session information retrieved successfully',
            'data': {
                'id': self.id,
                'name': self.name,
                'start_date': self.start_date,
                'duration': self.duration,
                'seat_total': self.seat_total,
                'seat_occupied': self.seat_occupied,
                'attendee_count': self.attendee_count,
                'state': self.state,
                'course': {
                    'id': self.course_id.id,
                    'name': self.course_id.name
                },
                'instructor': {
                    'id': self.partner_id.id,
                    'name': self.partner_id.name
                },
                'attendees': [{'id': attendee.id, 'name': attendee.name} for attendee in self.attendee_ids]
            }
        }

