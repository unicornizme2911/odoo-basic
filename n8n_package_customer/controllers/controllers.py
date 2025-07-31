# -*- coding: utf-8 -*-
# from odoo import http


# class N8nPackageCustomer(http.Controller):
#     @http.route('/n8n_package_customer/n8n_package_customer', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/n8n_package_customer/n8n_package_customer/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('n8n_package_customer.listing', {
#             'root': '/n8n_package_customer/n8n_package_customer',
#             'objects': http.request.env['n8n_package_customer.n8n_package_customer'].search([]),
#         })

#     @http.route('/n8n_package_customer/n8n_package_customer/objects/<model("n8n_package_customer.n8n_package_customer"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('n8n_package_customer.object', {
#             'object': obj
#         })

