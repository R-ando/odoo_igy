# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

#   Add_image
    image = fields.Binary('Image')

#   Sale_inherit
    mesure = fields.Char(
        string="Dimension",
        compute='_get_mesure')

#   Mrp_Fiche de débit
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

#   Sale_inherit
    @api.depends('largeur', 'hauteur')
    def _get_mesure(self):
        for line in self:
            line.mesure = str(int(line.largeur)) + "  x  " + str(int(line.hauteur))


class SaleOrder(models.Model):
    _inherit = 'sale.order'

#   Basique
    entete = fields.Text(
        string="Sujet")
#   Add_image
    note = fields.Text(
        string="Terms and conditions")
#   Majoration
    monnaie_lettre = fields.Char(
        string="Total en lettre",
        size=128)
    maj_globale = fields.Float(
        string="Majoration globale",
        default=0.0)
    maj_note = fields.Text(
        string="Note sur majoration")
#   Ajout crm_lead
    crm_lead_id = fields.Many2one(
        string="Opportunité",
        comodel_name="crm.lead",
        select=True,
        track_visibility='onchange')

#   Basique
    @api.multi
    def action_config_order_line(self):
        self.ensure_one()
        ctx = dict()
        sujet = 'Devis ' + self.name
        ctx.update({
            'default_sujet': sujet,
            'default_order_id': self.id,
        })
        return {
            'name': _('Configuration article'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order.line.advance',
            'target': 'new',
            'context': ctx,
        }

#   Majoration
#   Ajout de commmentaire si la/les majorations existent
    @api.model
    def create(self, vals):
        res_id = super(SaleOrder, self).create(vals)
        major1 = self.partner_id.major1
        major2 = self.user_id.major2
#        maj_globale = self.company_id.maj_globale

        majoration_text = ""

        if(major1 != 0.0 or major2 != 0.0):
            majoration_text += "Conforme aux calculs"
            self.message_post(res_id, body=majoration_text)
        return res_id
