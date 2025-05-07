from odoo import models, fields, api

class Faculty(models.Model):
    _name = 'faculty.info'
    _description = 'Faculty Information'

    name = fields.Char(string='Tên khoa', required=True)
    school_ids = fields.Many2many('school.info','school_faculty_rel',
                                  'faculty_id','school_id',string='Trường')
    major_ids = fields.One2many('major.info', 'faculty_id', string='Các chuyên ngành')