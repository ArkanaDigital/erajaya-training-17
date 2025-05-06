from odoo import models, fields, api, _


class Course(models.Model):
    _name = 'course.course'
    _description = 'Course'

    # day 1 - phase 1
    name = fields.Char(string='Title')
    description = fields.Text(string='Description')
    duration = fields.Integer(string='Duration (hours)')
    start_date = fields.Date(string='Start Date')

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
    start_date = fields.Date(string='Start Date')
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
        default=lambda self: self.env.user, index=True)
    session_ids = fields.One2many(
        comodel_name='course.session',
        inverse_name='course_id',
        string='Sessions'
    )

    active = fields.Boolean(default=True)
    is_to_delete = fields.Boolean()

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
