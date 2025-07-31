from odoo import models, fields

class ChatbotConversation(models.Model):
    _name = 'chatbot.conversation'
    _description = 'Chatbot Conversation'

    name = fields.Char(string='New Chat', required=True)
    user_id = fields.Many2one('res.users', string='User', required=True)
    message_ids = fields.One2many('chatbot.message', 'conversation_id', string='Messages')
    active = fields.Boolean(string='Active', default=True)