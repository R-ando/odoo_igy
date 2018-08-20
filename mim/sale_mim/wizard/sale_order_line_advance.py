# -*- coding: utf-8 -*-

from odoo import api, fields, models
import odoo.addons.decimal_precision as dp


class SaleOrderLineaAdvance(models.TransientModel):
    _name = 'sale.order.line.advance'
    _description = 'Product configuration'
    
    order_id = fields.Many2one('sale.order.line', 'Order line')
    sujet = fields.Char('Sujet', readonly=True)
    select_type = fields.Many2one('product.product', 'Type', domain=[('categ_id', '=', 3)], change_default=True)
    largeur = fields.Float('Largeur')
    hauteur = fields.Float('Hauteur')
    dimension = fields.Float('Dimension')
    pu_ttc = fields.Float('PU TTC')
    quantity = fields.Integer('Quantité')
    vitre = fields.Many2one('mim.article', string='Vitre', domain=[('category_id', '=', 'Vitrage')])
    type_vitre = fields.Selection([('simple', 'Simple'), ('double', 'Double')], string="")
    decoratif = fields.Many2one('mim.article', string='Décoratif', domain=[('category_id', '=', 'Decoratif')])
    poigne = fields.Many2one('mim.article', string='Poignée', domain=[('category_id', '=', 'Poignee')])
    nb_poigne = fields.Integer('Nombre')
    serr = fields.Many2one('mim.article', string='Serrure', domain=[('category_id', '=', 'Serrure')])
    nb_serr = fields.Integer('Nombre')
    oscillo_battant = fields.Boolean('Oscillo-battant')
    va_et_vient = fields.Boolean('Va et vient')
    butoir = fields.Boolean('Butoir')
    remplissage_vitre = fields.Selection([('standard', 'Standard'), ('pleine_2_3', '2/3 pleine'), ('pleine_1_2', '1/2 pleine'),
                                          ('pleine_1_3', '1/3 pleine'), ('pleine_bardage', 'Pleine/bardage')], string='Remplissage vitre')
    type_fixe = fields.Selection([('imposte', 'Imposte'), ('soubassement', 'Soubassement'), ('lateral', u'Latéral')], string='Type Fixe')
    inegalite = fields.Selection([('egaux', 'Egaux'), ('inegaux', u'Inégaux')], string=u"Inégalité")
    type_poteau = fields.Selection([('poteau_rect', 'Poteau rectangle'), ('poteau_angle', 'Poteau d\'angle'), ('tendeur', 'Tendeur')], string="Poteau Rect / Angle / Tendeur")
    cintre = fields.Boolean('Cintré')
    triangle = fields.Boolean('Triangle')
    division = fields.Boolean('Division')
    nb_division = fields.Integer('Nombre division')
    laque = fields.Boolean('Laqué')
    moustiquaire = fields.Boolean('Moustiquaire')
    tms = fields.Float('TMS')
    type_moustiquaire = fields.Selection([('fixe', 'Fixe'), ('coulissante', 'Coulissante')], string='Type de moustiquaire')
    total = fields.Float('Total', readonly=True, digits=dp.get_precision('Account'))
    totalcacher = fields.Float('Total')
    hidder_autre_option = fields.Boolean('Cacher les autres options')
    cacher = fields.Boolean('Cacher')
    intermediaire = fields.Selection([('sans', u'Sans intermédiaire'), ('avec', u'Avec intermédiaire')], string=u'Intermédiaire')
