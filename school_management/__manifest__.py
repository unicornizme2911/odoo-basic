# -*- coding: utf-8 -*-
{
    'name': "School Management",

    'summary': "Manage students, classes, and teachers in a school environment.",

    'description': """
School Management System
========================
This module allows you to manage school-related activities such as:
- Students information
- Teachers
- Classes
- Subjects
- Timetables
    """,

    'author': "My Company",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Education',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/school_info.xml',
        'views/faculty_info.xml',
        'views/student_info.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

