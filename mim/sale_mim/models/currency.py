# -*- coding: utf-8 -*-

from odoo import models, fields


class Currency(models.Model):
    _inherit = 'res.currency'

#   Add_image
    currency_name = fields.Char(
        string="Nom complet devise",
        size=20)
