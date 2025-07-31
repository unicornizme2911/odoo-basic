from odoo import http
from odoo.http import request
import json, requests, logging

_logger = logging.getLogger(__name__)

class ChatUIController(http.Controller):
    @http.route('/chat_ui', type='http', auth='user', website=True)
    def chat_ui(self, conversation_id=None, **kwargs):
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

        conversation_view_data = []
        for conv in conversations:
            last_msg = conv.message_ids.sorted('create_date')[-1] if conv.message_ids else None
            conversation_view_data.append({
                'id': conv.id,
                'name': conv.name,
                'last_message_content': last_msg.content if last_msg else '',
                'last_message_time': last_msg.timestamp.strftime('%H:%M') if last_msg and last_msg.timestamp else '',
            })

        return request.render('chat_module.chat_template', {
            'conversation_id': conversation.id if conversation else False,
            'messages': messages,
            'conversations': conversation_view_data,
            'current_conversation': conversation,
            'user_id': request.env.user.id,
            'conversation_data': json.dumps([
                {
                    'id': conv.id,
                    'name': conv.name,
                    'avatar': 'bg-primary',
                    'status': 'Đang hoạt động',
                    'messages': [
                        {
                            'id': msg.id,
                            'content': msg.content,
                            'time': msg.timestamp.strftime('%H:%M'),
                            'sent': True if msg.role == 'user' else False,
                            'image': msg.image_base64,
                        } for msg in conv.message_ids.sorted('create_date')
                    ]
                } for conv in conversations
            ])
        })

    @http.route('/chatbot/new', type='json', auth='user', methods=['POST'], website=True, csrf=False)
    def create_new_conversation(self, message=None, **kwargs):
        user = request.env.user
        new_conversation = request.env['chatbot.conversation'].sudo().create({
            'name': 'New Chat',
            'user_id': user.id
        })

        return {
            'id': new_conversation.id,
            'name': new_conversation.name
        }

    @http.route('/chatbot/send', type='json', auth='user', csrf=False)
    def send_message(self, **kwargs):
        try:
            raw_body = request.httprequest.data
            data = json.loads(raw_body)
        except Exception as e:
            return {'error': f'Invalid JSON body: {str(e)}'}

        content = data.get('content')
        conversation_id = data.get('conversation_id')
        user_id = request.env.user.id

        if not content or not content.strip():
            return {'error': 'Message cannot be empty'}

        chatbot_conversation = request.env['chatbot.conversation'].sudo()
        chatbot_message = request.env['chatbot.message'].sudo()

        conversation = chatbot_conversation.browse(int(conversation_id)) if conversation_id else None
        # Nếu không có conversation => tạo conversation mới
        if not conversation or not conversation.exists() or conversation.user_id.id != user_id:
            conversation = chatbot_conversation.create({
                'name': (content or 'New Chat')[:30],
                'user_id': user_id
            })
        print(conversation)
        message_user = chatbot_message.create({
            'conversation_id': conversation.id,
            'role': 'user',
            'content': content,
            'sender_id': user_id,
        })

        # 👉 Đảm bảo ghi vào DB
        request.env.cr.flush()

        # Nếu bạn muốn đảm bảo hơn nữa:
        request.env.cr.commit()

        # Lấy URL webhook từ cấu hình
        webhook_url = request.env['ir.config_parameter'].sudo().get_param(
            'chatbot_n8n.webhook_url'
        ) or 'http://localhost:5678/webhook/odoo_chatbot'
        # Sau đó gọi webhook
        try:
            res = requests.post(
                webhook_url,
                json={
                    'conversation_id': conversation.id,
                    'message_id': message_user.id,
                    'message': content,
                    'user_id': user_id,
                }
            )
            res.raise_for_status()
            bot_data = res.json()
            bot_reply = bot_data.get('output', 'No response from bot')
            image_base64 = bot_data.get('image')
            bot_name = bot_data.get('name', '')
            if image_base64:
                bot_reply = f'Đây là hình ảnh của {bot_name}'
        except Exception as e:
            bot_reply = f'Lỗi webhook: {str(e)}'
            image_base64 = None

        # Lưu phản hồi bot vào DB
        chatbot_message.create({
            'conversation_id': conversation.id,
            'role': 'bot',
            'content': bot_reply,
            'sender_id': user_id,
            'image_base64': image_base64,
        })

        return {
            'reply': bot_reply,
            'image_base64': image_base64,
            'conversation_id': conversation.id
        }