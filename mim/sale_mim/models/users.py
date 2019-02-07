# -*- coding: utf-8 -*-

from odoo import models, fields


class Users(models.Model):
    _inherit = 'res.users'

#   Majoration
    major2 = fields.Float(
        string="Majoration du Vendeur",
        default=0.0)
