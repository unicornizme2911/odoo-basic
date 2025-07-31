from odoo import models, fields, api

class ChatbotMessage(models.Model):
    _name = 'chatbot.message'
    _description = 'Chatbot Message'
    _order = 'create_date asc'

    conversation_id = fields.Many2one('chatbot.conversation', string='Conversation', required=True)
    role = fields.Selection([('user', 'User'), ('bot', 'Bot')], required=True)
    content = fields.Text(string='Content', required=True)
    timestamp = fields.Datetime(string='Timestamp', default=fields.Datetime.now, required=True)

    @api.model
    def create(self, vals):
        if 'conversation_id' not in vals or not vals['conversation_id']:
            raise ValueError("Conversation ID is required to create a message.")
        return super(ChatbotMessage, self).create(vals)