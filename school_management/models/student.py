from odoo import models, fields, api

class Student(models.Model):
    _name = 'student.info'
    _description = 'Student Information'
    _order = 'mssv desc'

    mssv = fields.Char(string='MSSV', required=True, copy=False, index=True, readonly=True,  store=True)
    name = fields.Char(string='Họ tên', required=True)
    avatar = fields.Binary(string='Avatar')
    day_of_birth = fields.Date(string='Ngày sinh', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='SĐT', required=True)
    gpa = fields.Float(string='GPA', default=0, compute='_compute_gpa', store=True)
    school_id = fields.Many2one('school.info', string="Trường", required=True, ondelete='restrict')
    major_id = fields.Many2one('major.info', string='Chuyên ngành', required=True, ondelete='restrict')
    enrollment_ids = fields.One2many('enrollment.info', 'student_id', string='Các môn học đã đăng ký')

    _sql_constraints = [
        ('unique_mssv', 'unique(mssv)', 'MSSV phải là duy nhất!')  # Enforce uniqueness
    ]

    @api.model
    def create(self, vals):
        major_id = vals.get('major_id')
        if major_id:
            major_id_str = str(major_id)
            prefix_len = len(major_id_str)
            suffix_len = 8 - prefix_len

            last_student = self.search(
                [('major_id', '=', major_id), ('mssv', 'like', f'{major_id_str}%')],
                order='mssv desc',
                limit=1
            )

            if last_student:
                next_student = str(int(last_student.mssv) + 1)
            else:
                next_student = major_id_str + '0'*(suffix_len - 1) + '1'

            vals['mssv'] = next_student

        return super(Student, self).create(vals)

    @api.depends('enrollment_ids.grade')
    def _compute_gpa(self):
        for student in self:
            grades = student.enrollment_ids.mapped('grade')
            if grades:
                student.gpa = sum(grades) / len(grades)
            else:
                student.gpa = 0