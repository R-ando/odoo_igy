# -*- coding: utf-8 -*-
from odoo import http

# class MrpMim(http.Controller):
#     @http.route('/mrp_mim/mrp_mim/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrp_mim/mrp_mim/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrp_mim.listing', {
#             'root': '/mrp_mim/mrp_mim',
#             'objects': http.request.env['mrp_mim.mrp_mim'].search([]),
#         })

#     @http.route('/mrp_mim/mrp_mim/objects/<model("mrp_mim.mrp_mim"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrp_mim.object', {
#             'object': obj
#         })