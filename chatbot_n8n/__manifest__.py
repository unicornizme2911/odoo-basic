# -*- coding: utf-8 -*-
{
    'name': "Chatbot N8N Integration",
    'summary': "Send messages to n8n and receive replies",
    'description': """
    This module allows you to send messages to n8n workflows and receive replies directly in Odoo.
    """,
    'author': "Cloudemedia",
    'website': "https://cloudmedia.vn",
    'category': 'Uncategorized',
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/chatbot_templates.xml',
        'views/chatbot_menu.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'chatbot_n8n/static/src/js/chatbot.js',
        ],
    },
    'application': True,
    'installable': True
}
