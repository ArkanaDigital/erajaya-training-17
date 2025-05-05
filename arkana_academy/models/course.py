from odoo import models, fields, api


class Course(models.Model):
    _name = 'course.course'
    _description = 'Course'


    # day 1
    name = fields.Char(string='Title')
    description = fields.Text(string='Description')
    duration = fields.Integer(string='Duration (hours)')
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
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    enrollment_deadline = fields.Datetime(string='Enrollment Deadline')
    price = fields.Monetary(
        string='Price',
        currency_field='currency_id',
        help='Course Price',
        groups=False
    )
    is_edit_price = fields.Boolean(
        string='Is Edit Price', compute='_compute_is_edit_price'
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency'
    )
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
        default=lambda self: self.env.user)
    session_ids = fields.One2many(
        comodel_name='course.session',
        inverse_name='course_id',
        string='Sessions'
    )
    is_publish = fields.Boolean(string='Published', default=True)

    _sql_constraints = [('name_unique', 'UNIQUE(name)', 'Session name must be unique')]

    @api.depends('duration')
    def _compute_display_name(self):
        for course in self:
            if self.env.context.get('show_course_duration'):
                course.display_name = f"{course.name} - {str(course.duration)}"
            else:
                return super()._compute_display_name()

    def _compute_is_edit_price(self):
        for rec in self:
            rec.is_edit_price = True if self.env.user.has_group('arkana_academy.group_academy_manager') else False

    def action_enrollment(self):
        self.write({'state': 'enrollment'})

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        self.write({'state': 'done'})

    def copy(self, default=None):
        default = dict(default or {})
        default['name'] = ''
        return super(Course, self).copy(default)
