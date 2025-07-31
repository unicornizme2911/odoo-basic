from odoo import http
from odoo.http import request
import requests
import json

class ChatbotController(http.Controller):
    @http.route('/chatbot', type='http', auth='user', website=True)
    def chatbot_ui(self, conversation_id=None, **kwargs):
        Conversation = request.env['chatbot.conversation'].sudo()
        domain = [('user_id', '=', request.env.user.id)]
        conversations = Conversation.search(domain, order='id desc')

        conversation = None
        if conversation_id:
            conversation = Conversation.browse(int(conversation_id))
            if not conversation.exists():
                conversation = None
        elif conversations and len(conversations) > 0:
            conversation = conversations[0]

        messages = conversation.message_ids.sorted(key=lambda m: m.create_date) if conversation else []

        return request.render('chatbot_n8n.chatbot_ui', {
            'conversation_id': conversation.id if conversation else False,
            'messages': messages,
            'conversations': conversations,
            'current_conversation': conversation
        })

    @http.route('/chatbot/new', auth='user', methods=['POST'], website=True, csrf=True)
    def chatbot_new(self, **post):
        new_conversation = request.env['chatbot.conversation'].sudo().create({
            'name': 'New Chat',
            'user_id': request.env.user.id
        })
        return request.redirect(f'/chatbot?conversation_id={new_conversation.id}')

    @http.route('/chatbot/send', type='json', auth='user', csrf=False)
    def send_message(self, **kwargs):
        try:
            raw_body = request.httprequest.data
            data = json.loads(raw_body)
        except Exception as e:
            return {'error': f'Invalid JSON body: {str(e)}'}

        content = data.get('content')
        conversation_id = data.get('conversation_id')
        print(content, conversation_id)
        if not content or not content.strip():
            return {'error': 'Message cannot be empty'}
        chatbot_conversation = request.env['chatbot.conversation'].sudo()
        chatbot_message = request.env['chatbot.message'].sudo()
        conversation = chatbot_conversation.browse(int(conversation_id)) if conversation_id else None
        # Nếu không có conversation => tạo conversation mới
        if not conversation or not conversation.exists() or conversation.user_id.id != request.env.user.id:
            conversation = chatbot_conversation.create({
                'name': (content or 'New Chat')[:30],
                'user_id': request.env.user.id
            })

        chatbot_message.create({
            'conversation_id': conversation.id,
            'role': 'user',
            'content': content
        })
        webhook_url = request.env['ir.config_parameter'].sudo().get_param('chatbot_n8n.webhook_url') or 'https://n8n.cloudmedia.vn/webhook/odoo'

        try:
            res = requests.post(
                webhook_url,
                json={
                    'message': content,
                    'conversation_id': conversation.id,
                    'user_id': request.env.user.id
                },
                timeout=5
            )
            res.raise_for_status()
            bot_reply = res.json().get('reply', 'No response from bot')
        except Exception as e:
            bot_reply = f'Error: {str(e)}'

        chatbot_message.create({
            'conversation_id': conversation.id,
            'role': 'bot',
            'content': bot_reply
        })
        return {'reply': bot_reply, 'conversation_id': conversation.id}