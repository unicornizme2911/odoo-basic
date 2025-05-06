# -*- coding: utf-8 -*-
# from odoo import http


# class SchoolManager(http.Controller):
#     @http.route('/school_manager/school_manager', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/school_manager/school_manager/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('school_manager.listing', {
#             'root': '/school_manager/school_manager',
#             'objects': http.request.env['school_manager.school_manager'].search([]),
#         })

#     @http.route('/school_manager/school_manager/objects/<model("school_manager.school_manager"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('school_manager.object', {
#             'object': obj
#         })

