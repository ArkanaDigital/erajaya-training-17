from odoo import models, fields, api, _
from datetime import date


DOMAIN_USER_ID = [('name', 'ilike', 'XXX')]

class Course(models.Model):
    _name = 'course.course'
    _description = 'Course'

    def default_start_date_first(self):
        return date.today()

    # day 1 - phase 1
    name = fields.Char(string='Title')
    description = fields.Text(string='Description')
    duration = fields.Integer(
        string='Duration (hours)',
        default=10,
    )

    # Day 1 - phase 2
    syllabus = fields.Html(
        string='Syllabus',
        sanitize=True,
        sanitize_tags=True,
        help='Course Syllabus with formatting'
    )
    level = fields.Selection([
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advance', 'Advance'),
        ('expert', 'Expert'),
    ], string='Level', default='beginner')

    start_date = fields.Date(
        string='Start Date',
        default=fields.Date.today,
        # default=lambda self: date.today(),
        # default=default_start_date_first,
        # default=lambda self: self.default_start_date_second(),
        tracking=True
    )
    end_date = fields.Date(string='End Date')
    enrollment_deadline = fields.Datetime(string='Enrollment Deadline')

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("enrollment", "Enrollment"),
            ("in_progress", "In Progress"),
            ("done", "Done")
        ], string='Status', default="draft"
    )

    # day 2
    user_id = fields.Many2one(
        'res.users',
        string='Responsible',
        domain=DOMAIN_USER_ID,
        default=lambda self: self.env.user, index=True
    )
    user_email = fields.Char(
        string="Responsible Email",
        compute='_compute_user_email',
        store=True
    )
    session_ids = fields.One2many(
        comodel_name='course.session',
        inverse_name='course_id',
        string='Sessions'
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        readonly=False,
        default=lambda self: self.env.company)
    active = fields.Boolean(default=True)
    is_to_delete = fields.Boolean()

    # @api.onchange('user_id')
    # @api.onchange()
    @api.depends('user_id', 'user_id.partner_id.email')
    def _compute_user_email(self):
        """
        Compute the email of the user responsible for the course.
        - each time user_id change, then user_email is recomputed
        - each time user_id.partner_id.email change, then user_email is recomputed
        """
        for record in self:
            if record.user_id:
                record.user_email = record.user_id.partner_id.email
            else:
                record.user_email = False

    @api.onchange('start_date')
    def _onchange_start_date(self):
        if self.start_date:
            self.end_date = self.start_date

    def default_start_date_second(self):
        return date.today()

    def button_publish(self):
        self.state = 'enrollment'
        return True

    def button_unpublish(self):
        self.state = 'draft'
        return True

    def unlink(self):
        for record in self:
            if record.state in ['enrollment']:
                raise models.ValidationError(
                    _("You can only delete courses in the 'Enrollment' state.")
                )
        return super(Course, self).unlink()
