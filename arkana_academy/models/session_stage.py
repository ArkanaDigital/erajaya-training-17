from odoo import models, fields

class SessionStage(models.Model):
    _name = 'course.session.stage'
    _description = 'Session Stage'
    _order = 'sequence, id'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    fold = fields.Boolean()
    active = fields.Boolean(default=True)
