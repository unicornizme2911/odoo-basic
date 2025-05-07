from odoo import models, fields, api

class Major(models.Model):
    _name = 'major.info'
    _description = 'Major Info'

    name = fields.Char(string='Tên chuyên ngành', required=True)
    description = fields.Text(string='Mô tả')
    faculty_id = fields.Many2one('faculty.info', string='Khoa', required=True, ondelete='restrict')
    subject_ids = fields.One2many('subject.info', 'major_id', string='Các môn học')
    student_ids = fields.One2many('student.info', 'major_id', string='Sinh viên')