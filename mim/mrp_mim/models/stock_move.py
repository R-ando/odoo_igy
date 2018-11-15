# -*- coding: utf-8 -*-

from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    id_mo = fields.Integer(
        string="Id manufacturing order")
    is_mo_created = fields.Boolean(
        string="Ordre de fabrication créé",
        default=False)
    is_printable = fields.Boolean(
        string="Fiche de débit standard",
        default=False)

    largeur = fields.Float(
        string="Largeur")
    hauteur = fields.Float(
        string="Hauteur")
