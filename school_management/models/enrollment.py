from odoo import models, fields, api

class Enrollment(models.Model):
    _name = 'enrollment.info'
    _description = 'Enrollment Information'

    student_id = fields.Many2one('student.info',string='Sinh viên', required=True, ondelete='restrict')
    subject_id = fields.Many2one('subject.info',string='Môn học', required=True, ondelete='restrict')
    enrollment_date = fields.Datetime(string='Ngày đăng ký', default=fields.Datetime.now)
    grade = fields.Float(string='Điểm số', digits=(0, 2), default=0)

    _sql_constraints = [
        ('unique_student_subject', 'unique(student_id,subject_id)', 'Một sinh viên không thể đăng ký cùng một môn học nhiều lần.')
    ]