from odoo import models, fields, tools

class CourseStatisticsView(models.Model):
    _name = 'course.statistics.view'
    _description = 'Course Statistics View'
    _auto = False  # This tells Odoo this is not a regular table
    _order = 'total_attendees desc'

    name = fields.Char('Course Name')
    level = fields.Selection([
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advance', 'Advance'),
        ('expert', 'Expert'),
    ], string='Level')
    total_sessions = fields.Integer('Total Sessions')
    total_attendees = fields.Integer('Total Attendees')
    total_duration = fields.Float('Total Duration')
    avg_occupancy = fields.Float('Average Occupancy (%)')
    course_state = fields.Selection([
        ("draft", "Draft"),
        ("enrollment", "Enrollment"),
        ("in_progress", "In Progress"),
        ("done", "Done")
    ], string='Course Status')

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    c.id,
                    c.name,
                    c.level,
                    c.state as course_state,
                    COUNT(DISTINCT s.id) as total_sessions,
                    COALESCE(SUM(s.attendee_count), 0) as total_attendees,
                    COALESCE(SUM(s.duration), 0) as total_duration,
                    CASE 
                        WHEN COUNT(s.id) > 0 THEN 
                            AVG(COALESCE(s.seat_occupied, 0))
                        ELSE 0 
                    END as avg_occupancy
                FROM 
                    course_course c
                LEFT JOIN 
                    course_session s ON s.course_id = c.id
                GROUP BY
                    c.id,
                    c.name,
                    c.level,
                    c.state
            )
        """ % (self._table,))
