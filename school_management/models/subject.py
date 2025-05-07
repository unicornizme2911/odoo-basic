from odoo import models, fields, api

class Subject(models.Model):
    _name = 'subject.info'
    _description = 'Subject Information'

    name = fields.Char(string='Tên môn học', required=True)
    credits = fields.Integer(string='Số tín chỉ', required=True)
    rank = fields.Integer(string='Cấp bậc')
    major_id = fields.Many2one('major.info', string='Chuyên ngành', required=True, ondelete='restrict')
    enrollment_ids = fields.One2many('enrollment.info', 'subject_id', string='Lớp học')