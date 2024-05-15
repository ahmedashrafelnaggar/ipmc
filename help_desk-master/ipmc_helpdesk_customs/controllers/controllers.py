# -*- coding: utf-8 -*-
# from odoo import http


# class HelpDesk(http.Controller):
#     @http.route('/help_desk/help_desk', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/help_desk/help_desk/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('help_desk.listing', {
#             'root': '/help_desk/help_desk',
#             'objects': http.request.env['help_desk.help_desk'].search([]),
#         })

#     @http.route('/help_desk/help_desk/objects/<model("help_desk.help_desk"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('help_desk.object', {
#             'object': obj
#         })
