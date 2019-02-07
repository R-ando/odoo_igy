# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    largeur = fields.Float(
        string="Largeur")
    hauteur = fields.Float(
        string="Hauteur")
    dimension = fields.Float(
        string="Dimension")
    vitre = fields.Many2one(
        string="Vitre",
        comodel_name="mim.article")
    type_vitre = fields.Selection(
        string="Type de vitre",
        selection=[
            ('simple', 'Simple'),
            ('double', 'Double')])
    decoratif = fields.Many2one(
        string=u"Décoratif",
        comodel_name="mim.article")
    poigne = fields.Many2one(
        string=u"Poignée",
        comodel_name="mim.article")
    nb_poigne = fields.Integer(
        string="Nombre")
    serr = fields.Many2one(
        string="Serrure",
        comodel_name="mim.article")
    nb_serr = fields.Integer(
        string="Nombre")
    oscillo_battant = fields.Boolean(
        string="Oscillo-battant")
    va_et_vient = fields.Boolean(
        string="Va et vient")
    butoir = fields.Boolean(
        string="Butoir")
    remplissage_vitre = fields.Selection(
        string="Remplissage de vitre",
        selection=[
            ('standard', 'Standard'),
            ('pleine_2_3', '2/3 pleine'),
            ('pleine_1_2', '1/2 pleine'),
            ('pleine_1_3', '1/3 pleine'),
            ('pleine_bardage', 'Pleine/bardage')])
    type_fixe = fields.Selection(
        string="Type fixe",
        selection=[
            ('imposte', 'Imposte'),
            ('soubassement', 'Soubassement'),
            ('lateral', u'Latéral')])
    inegalite = fields.Selection(
        string=u"Inégalité",
        selection=[
            ('egaux', 'Egaux'),
            ('inegaux', u'Inégaux')])
    cintre = fields.Boolean(
        string=u"Cintré")
    triangle = fields.Boolean(
        string="Triangle")
    division = fields.Boolean(
        string="Division")
    nb_division = fields.Integer(
        string="Nombre division")
    laque = fields.Boolean(
        string=u"Laqué")
    moustiquaire = fields.Boolean(
        string="Moustiquaire")
    type_moustiquaire = fields.Selection(
        string="Type moustiquaire",
        selection=[
            ('fixe', 'Fixe'),
            ('coulissante', 'Coulissante')])
    tms = fields.Float(
        string="TMS")
    intermediaire = fields.Selection(
        string=u"Intermédiaire",
        selection=[
            ('sans', u'Sans intermédiaire'),
            ('avec', u'Avec intermédiaire')])
