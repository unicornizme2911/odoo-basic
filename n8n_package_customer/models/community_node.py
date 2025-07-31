from odoo import fields, models, api
import requests

class N8nCommunityNodeModelName(models.Model):
    _name = 'n8n.community.node'
    _description = 'Node community cho N8N'

    name = fields.Char(string='Tên gói', required=True)
    description = fields.Text(string='Mô tả')
    npm_url = fields.Char(string='NPM URL')
    github_url = fields.Char(string='GitHub URL')

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Gói NPM này đã tồn tại!')
    ]

    @api.model
    def action_sync_from_npm(self, *args, **kwargs):
        url = "https://registry.npmjs.org/-/v1/search"
        params = {
            "text": "keywords:n8n-community-node-package",
            "size": 100
        }
        res = requests.get(url, params=params)
        if res.status_code != 200:
            raise Exception("Không thể truy cập NPM")

        data = res.json()
        print(data)
        for pkg in data.get("objects", []):
            pkg_data = pkg["package"]
            name = pkg_data.get("name")
            description = pkg_data.get("description")
            npm_url = pkg_data.get("links", {}).get("npm")
            github_url = pkg_data.get("links", {}).get("repository")

            existing = self.env['n8n.community.node'].search([('name', '=', name)], limit=1)
            if not existing:
                self.env['n8n.community.node'].create({
                    'name': name,
                    'description': description,
                    'npm_url': npm_url,
                    'github_url': github_url,
                })
            else:
                existing.write({
                    'description': description,
                    'npm_url': npm_url,
                    'github_url': github_url,
                })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'n8n.community.node',
            'view_mode': 'tree,form',
            'target': 'current',
        }