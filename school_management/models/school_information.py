import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError

SCHOOL_PHONE_REGEX = re.compile(r'^0\d{9,10}$')
SCHOOL_EMAIL_REGEX = re.compile(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$')

class SchoolInformation(models.Model):
    _name = 'school.information'
    _description = 'School Information'

    name = fields.Char(string='Tên trường', required=True)
    type = fields.Selection(string='Loại trường', selection=[('private','Tư lập'),('public','Công lập')], default='public')
    email = fields.Text(string='Email', required=True)
    address = fields.Text(string='Địa chỉ', required=True)
    phone = fields.Char(string='SĐT', required=True)

    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if record.phone and not SCHOOL_PHONE_REGEX.match(record.phone):
                raise ValidationError("SĐT không hợp lệ. Vui lòng nhập số bắt đầu bằng 0 và có 10 hoặc 11 chữ số.")

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and not SCHOOL_EMAIL_REGEX.match(record.email):
                raise ValidationError("Email không hợp lệ. Vui lòng nhập đúng định dạng.")