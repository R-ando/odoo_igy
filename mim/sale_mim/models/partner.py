# -*- coding: utf-8 -*-

from odoo import models, fields


class Partner(models.Model):
    _inherit = 'res.partner'

#   Majoration
    major1 = fields.Float(
        string="Majoration du Client",
        default=0.0)
