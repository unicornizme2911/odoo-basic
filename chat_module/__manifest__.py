{
    "name": "Odoo Chat",
    "version": "1.0",
    "author": "Sơn",
    "category": "Tools",
    "data": [
        "security/ir.model.access.csv",
        'views/menu.xml',
        'views/chat_template.xml',
    ],
    'depends': ['base', 'web',],
    # 'assets': {
    #     'web.assets_backend': [
    #         'chat_module/static/src/js/chat.js',
    #         'chat_module/static/src/xml/chat_template.xml',
    #     ],
    # },
    'assets': {
        'web.assets_frontend': [
            'chat_module/static/src/css/chat.css',
            # 'chat_module/static/src/js/chat.js'
        ],
    },

    "installable": True,
    "application": True,
}
