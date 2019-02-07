# -*- coding: utf-8 -*-

from odoo import models, fields


class Company(models.Model):
    _inherit = 'res.company'

#   Majoration
    maj_globale = fields.Float(
        string="Majoration globale",
        default=0.0)
    maj_note = fields.Text(
        string="Note sur la majoration")
