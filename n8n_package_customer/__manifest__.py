# -*- coding: utf-8 -*-
{
    'name': "n8n Package Customer",

    'summary': "Quản lý khách hàng mua gói dịch vụ n8n",

    'description': """
Lưu trữ thông tin và quản lý khách hàng mua dịch vụ n8n
    """,

    'author': "Cloudemedia",
    'website': "https://cloudmedia.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/customer_views.xml',
        'views/package_order_views.xml',
        'views/community_node_views.xml'
    ],
    # only loaded in demonstration mode
    'application': True,
    'installable': True
}

