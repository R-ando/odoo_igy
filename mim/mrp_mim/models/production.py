# -*- coding: utf-8 -*-
<<<<<<< HEAD

from odoo import models, fields, api, exceptions
=======
import logging

from math import ceil as ceil

from odoo import models
from odoo import fields
from odoo import api
from odoo import exceptions


_logger = logging.getLogger(__name__)

>>>>>>> 5bec217211feeae309b49c6f249c9e8946e85c8a

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    largeur = fields.Float(
<<<<<<< HEAD
        string="Largeur")
=======
        string="Largeur")   
>>>>>>> 5bec217211feeae309b49c6f249c9e8946e85c8a
    hauteur = fields.Float(
        string="Hauteur")
    nbr_barre = fields.Float(
        string="Nombre total de barres")
    # product_lines1 = fields.One2many(
    #     string="Articles",
    #     comodel_name="mrp.production.product.component.line",
<<<<<<< HEAD
    #     inverse_name="production_iimport ipdb; ipdb.set_trace()d")
=======
    #     inverse_name="production_id")
>>>>>>> 5bec217211feeae309b49c6f249c9e8946e85c8a
    # product_lines2 = fields.One2many(
    #     string="Accessoires",
    #     comodel_name="mrp.production.product.accessory.line",
    #     inverse_name="production_id")
    is_printable = fields.Boolean(
        string="Fiche de débit standard",
        default=False)
    dimension = fields.Float(
        string="Dimension")
    vitre = fields.Many2one(
        string="Vitre",
        comodel_name="mim.article",
        domain=[('category_id', '=', 'Vitrage')])
    type_vitre = fields.Selection(
        string="Type de vitre",
        selection=[
            ('simple', 'Simple'),
            ('double', 'Double')])
    decoratif = fields.Many2one(
        string="Décoratif",
        comodel_name="mim.article",
        domain=[('category_id', '=', 'Decoratif')])
    poigne = fields.Many2one(
        string="Poignée",
        comodel_name="mim.article",
        domain=[('category_id', '=', 'Poignee')])
    nb_poigne = fields.Integer(
        string="Nombre")
    serr = fields.Many2one(
        string="Serrure",
        comodel_name="mim.article",
        domain=[('category_id.name', '=', 'Serrure')])
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
<<<<<<< HEAD

    tms = fields.Float(string="TMS")
=======
    tms = fields.Float(
        string="TMS")
>>>>>>> 5bec217211feeae309b49c6f249c9e8946e85c8a
    intermediaire = fields.Selection(
        string=u"Intermédiaire",
        selection=[
            ('sans', u'Sans intermédiaire'),
            ('avec', u'Avec intermédiaire')])
    type_intermediaire = fields.Selection(
        string="Type d\'intermédiaire",
        selection=[
            ('vertical', 'Vertical'),
            ('horizontal', 'Horizontal')])
    is_calculated = fields.Boolean(
        string="Fiche de débit calculée",
        default=False)
    longueur_barre = fields.Float(
        string="Longueur barre",
        default=5800.0)
    description = fields.Char(
        string="Description")
    partner_id = fields.Many2one(
        string="Partenaire",
        comodel_name="res.partner")
    style = fields.Selection(
        string="Style",
        selection=[
            ('fr', u'A la française'),
            ('en', 'A l\'anglaise')],
        default='fr'
    )
    # batis_id = fields.Many2one(
    #     string=u"Bâtis",
    #     comodel_name="mim.article",
    #     domain=[('category_id', '=', u'Bâtis')])

    state = fields.Selection(
        string="Statut",
        selection=[
            ('confirmed', 'Confirmed'),
            ('verified', u'Fiche vérifiée'),
            ('validated', u'Fiche de débit validée'),
            ('picking_except', 'Picking Exception'),
            ('planned', 'Planned'),
            ('progress', 'In Progress'),
            ('done', 'Done'),
            ('cancel', 'Cancelled')])
    date_planned = fields.Datetime(
        string=u"Date Plannifié",
        required=True,
        select=1,
        readonly=False,
        states={'done': [('readonly', True)]})
    # product_lines = fields.One2many(
    #     string="Scheduled goods",
    #     comodel_name="mrp.production.product.line",
    #     inverse_name="production_id",
    #     readonly=True,
    #     states={'confirmed': [('readonly', False)]})
    partner_name = fields.Char(
        string="Nom du client",
        compute='_get_partner_name')

<<<<<<< HEAD
    @api.multi
    def change_etat_to_fiche_verifie(self):
        self.write({
            'state' : 'Fiche vérifiée',
            })
        return True

    @api.depends('partner_id')
    def _get_partner_name(self):
        for production in self:
            production.partner_name = production.partner_id.name

    #CPR
    # def _get_default_basis(self):
    # batis_ids = self.env['mim.article'].search([('name', '=', 'T 60 K B')])
    # if not batis_ids:
    #     raise osv.except_osv('Erreur!', u"Le bâtis T 60 K B par défaut n\'est pas défini dans mim.article!")
    # return batis_ids[0]

    # def _get_partner_name(self):
    #     res = {}
    #     if context is None:
    #         context = {}
    #     for production in self.browse():
    #         res[production.id] = production.partner_id.name
    #     return res

    # def round_float(self, qty):
    #     s = str(qty)
    #     t = s.split('.')
    #     dec = 0
    #     if int(t[1])>0:
    #         dec = 1
    #     res = int(t[0]) + dec
    #     return res

    # def get_nbr_barres(self,qty_mm):
    #     len_barre = self.browse()[0].longueur_barre
    #     #len_barre est la longueur d'une barre en mm par unité
    #     qty_barres = qty_mm/len_barre
    #     return self.round_float(qty_barres)

    # def set_draft(self):
    # req = """UPDATE wkf_workitem w
    #     SET act_id = (SELECT a.id FROM wkf_activity a WHERE a.wkf_id=(SELECT wkf.id FROM wkf WHERE wkf.name='mrp.production.basic') AND a.name='draft')
    #     WHERE w.inst_id = (SELECT i.id FROM wkf_instance i WHERE i.res_id={0} AND i.res_type='mrp.production')""".format(ids[0])
    #     cr.execute(req)
    #     self.write({'state': 'draft'})
    #     return True


=======

    # <work_flow>
    @api.multi
    def verification(self):
        """mrp_fiche_de_debit
            mrp.py
            class mrp_production
            action_verified"""

        move_obj = self.env['stock.move']
        
        for prod in self:
            state_move = move_obj.search([('production_id', '=', prod.id)]).state
            if state_move != 'contre_mesure':
                raise exceptions.ValidationError(
                    u"Le mouvement lié à cet ordre fabrication n'est pas encore dans l'état contre-mesure"
                )
            if prod.hauteur == 0.0 or prod.largeur == 0.0:
                raise exceptions.ValidationError(
                    u"Les contre-mesures ne doivent pas être vides. Merci de faire remplir par le responsable dans le bon de livraison lié"
                )

        self.write({
            'state':'verified',
            })

    @api.multi
    def action_validation(self):
        self.write({
            'state':'validated'
        })

    # </work_flow>

    @api.multi
    def _get_nbr_barres(self, qty_mm):
        len_barre = self.longueur_barre
        qty_barres = qty_mm/len_barre
        return ceil(qty_barres)
>>>>>>> 5bec217211feeae309b49c6f249c9e8946e85c8a
