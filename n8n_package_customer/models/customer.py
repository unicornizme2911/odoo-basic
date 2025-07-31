from odoo import fields, models, api


class N8nPackageCustomer(models.Model):
    _name = 'n8n.package.customer'
    _description = 'Khách hàng gói dịch vụ N8N'

    name = fields.Char(string='Tên khách hàng', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Số điện thoại')
    notes = fields.Text(string='Ghi chú')
    package_order_ids = fields.One2many(
        'n8n.package.order',
        'customer_id',
        string='Gói dịch vụ đã mua'
    )