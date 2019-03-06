# -*- coding: utf-8 -*-
from odoo import http

# class PaieMim(http.Controller):
#     @http.route('/paie_mim/paie_mim/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/paie_mim/paie_mim/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('paie_mim.listing', {
#             'root': '/paie_mim/paie_mim',
#             'objects': http.request.env['paie_mim.paie_mim'].search([]),
#         })

#     @http.route('/paie_mim/paie_mim/objects/<model("paie_mim.paie_mim"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('paie_mim.object', {
#             'object': obj
#         })