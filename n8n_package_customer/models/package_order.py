from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import UserError
import requests

class N8nPackageOrder(models.Model):
    _name = 'n8n.package.order'
    _description = 'Gói dịch vụ N8N của khách hàng'

    customer_id = fields.Many2one(
        'n8n.package.customer',
        string='Khách hàng',
        required=True,
        ondelete='cascade'
    )
    package_name = fields.Char(string='Tên gói', required=True)
    start_date = fields.Date(string='Ngày bắt đầu', default=fields.Date.today)
    end_date = fields.Date(string='Ngày kết thúc')
    notes = fields.Text(string='Ghi chú')
    instance_status = fields.Selection([
        ('running', 'Đang chạy'),
        ('stopped', 'Đã dừng'),
        ('error', 'Lỗi')
    ], string='Trạng thái', default='stopped')

    domain = fields.Char(string='Domain / IP Instance')
    port = fields.Integer(string='Port')
    n8n_username = fields.Char(string='Tài khoản đăng nhập')
    n8n_password = fields.Char(string='Mật khẩu', password=True)

    node_community_ids = fields.Many2many(
        'n8n.community.node',
        'order_node_rel',
        'order_id',
        'node_id',
        string='Node community'
    )

    def action_install_node_community(self):
        for rec in self:
            if not rec.node_community_ids:
                raise UserError("Chưa chọn node community nào.")

            failed_nodes = []
            for node in rec.node_community_ids:
                payload = {
                    "node_name": node.name,
                    "instance": rec.package_name,  # hoặc dùng trường riêng nếu có
                }
                try:
                    response = requests.post("http://localhost:5000/install_node", json=payload)
                    if response.status_code != 200:
                        failed_nodes.append(node.name)
                except Exception as e:
                    failed_nodes.append(node.name)

            if failed_nodes:
                raise UserError(f"Các node sau cài không thành công: {', '.join(failed_nodes)}")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Thành công',
                    'message': 'Đã gửi yêu cầu cài node thành công!',
                    'type': 'success',
                    'sticky': False,
                }
            }
        return None

    @api.model
    def create(self, vals):
        if 'start_date' in vals and 'end_date' not in vals:
            vals['end_date'] = fields.Date.from_string(vals['start_date']) + timedelta(days=30)
        return super().create(vals)

    # def action_start_instance(self):
    #     self._call_instance_api('start')
    #
    # def action_stop_instance(self):
    #     self._call_instance_api('stop')
    #
    # def action_restart_instance(self):
    #     self._call_instance_api('restart')