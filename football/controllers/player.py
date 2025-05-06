import json
from odoo import api, fields, http
from odoo.http import request

class PlayerController(http.Controller):
    @http.route('/player', auth='public', website=True, type='http')
    def player(self):
        return "check"