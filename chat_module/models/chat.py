from odoo import models, fields

class ChatConversation(models.Model):
    _name = "chat.conversation"
    _description = "Chat Conversation"

    name = fields.Char("Conversation Name", required=True)
    message_ids = fields.One2many("chat.message", "conversation_id", string="Messages")

class ChatMessage(models.Model):
    _name = "chat.message"
    _description = "Chat Message"
    _order = "create_date asc"

    conversation_id = fields.Many2one("chat.conversation", required=True)
    content = fields.Text("Message")
    sender_id = fields.Many2one("res.users", string="Sender", default=lambda self: self.env.user)
    create_date = fields.Datetime("Created", readonly=True)
