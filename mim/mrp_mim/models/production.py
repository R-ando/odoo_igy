# -*- coding: utf-8 -*-
import logging

from math import ceil as ceil

from odoo import models
from odoo import fields
from odoo import api
from odoo import exceptions
from odoo.tools import safe_eval


_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    largeur = fields.Float(
        string="Largeur")   
    hauteur = fields.Float(
        string="Hauteur")
    nbr_barre = fields.Float(
        string="Nombre total de barres")
    # Product line for article and accessory
    product_lines1 = fields.One2many(
        string="Articles",
        comodel_name="mrp.production.product.component.line",
        inverse_name="production_id")
    product_lines2 = fields.One2many(
        string="Accessoires",
        comodel_name="mrp.production.product.accessory.line",
        inverse_name="production_id")
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
    tms = fields.Float(
        string="TMS")
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
    batis_id = fields.Many2one(
        string=u"Bâtis",
        comodel_name="mim.article",
        domain=[('category_id', '=', u'Bâtis')])

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
    # Ligne des produits pour la fabrication d'un article
    product_lines = fields.One2many(
        string="Scheduled goods",
        comodel_name="mrp.production.product.line",
        inverse_name="production_id",
        readonly=True,
        states={'confirmed': [('readonly', False)]})
    partner_name = fields.Char(
        string="Nom du client",
        compute='_get_partner_name')


    @api.depends('partner_id')
    def _get_partner_name(self):
        for production in self:
            production.partner_name = production.partner_id.name

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

    # <last_commit>

    # new method
    @api.multi
    def count_raw_materials(self, results):
        raw_materials_obj = self.env['mrp.rawmaterials.count']
        for result in results:
            # find if the product already exist
            product_obj = result[0]
            res_id = raw_materials_obj.search([('product_id', '=', product_obj.product_id.product_tmpl_id.id)])
            if res_id:
                # exist, then we update
                total_qty = res_id.product_qty + result[1]['qty']
                res_id.write({'product_qty': total_qty})
            else:
                # !exist, then we create
                data = {
                    'product_name': product_obj.product_id.product_tmpl_id.name,
                    'product_id': product_obj.product_id.product_tmpl_id.id,
                    'product_qty': result[1]['qty'],
                    'product_uom_id': product_obj.product_uom_id.id,
                    'product_uom_name': product_obj.product_uom_id.name,
                    'product_cat_name': product_obj.product_id.product_tmpl_id.categ_id.name
                }
                raw_materials_obj.create(data)


    # Retourne BOM structure
    @api.multi
    def prepare_lines(self, production, properties=None):
        bom_obj = self.env['mrp.bom']
        uom_obj = self.env['product.uom']
        bom_point = production.bom_id
        bom_id = production.bom_id.id
        if not bom_point:
            bom_id = bom_obj._bom_find(product_id=production.product_id.id)
            # bom_id = bom_obj._bom_find(product=self.production.product_id.id)
            if bom_id:
                bom_point = bom_obj.browse(bom_id)
                routing_id = bom_point.routing_id.id or False
                self.write(
                    [production.id],
                    {
                    'bom_id': bom_id,
                    'routing_id': routing_id,
                    }
                )
        if not bom_id:
            raise exceptions.ValidationError(
                u"Ne peut pas trouver le bilan de ce matériel"
                )
        # get components from BOM structure
        # factor = production.product_uom_id._compute_quantity(
        #     production.product_qty,bom_point.product_uom_id
        #     )/bom_point.product_qty
        factor = uom_obj._compute_quantity(
            production.product_uom_id.id,
            production.product_qty,
            bom_point.product_uom_id.id
        )
        boms = production.bom_id.bom_explode(
            production.product_id,
            factor,
            picking_type=production.bom_id.picking_type_id
            )
        _logger.info(boms)
        return boms
        # boms = bom_obj.bom_explode(
        #     bom_point,
        #     production.product_id,
        #     (factor/bom_point.product_qty)
        # )

        # _logger.info(boms)
        # return boms

    # Test si l'article a été consumé ou produit
    # Retourne True or False
    @api.multi
    def test_if_product(self):
        res = True
        if self.is_printable:
            for production in self:
                boms = self.prepare_lines(production)
                res = False
                for bom in boms:
                    product = self.env['product.product'].browse(bom['product_id'])
                    if product.type in ('product','consu'):
                        res = True
        return res
    
    # Test si move_raw_ids est prêt ou non
    @api.multi
    def test_ready(self):
        res = True
        for production in self:
            if production.move_raw_ids and not production.ready_production:
                res = False

        return res
    
    # Fonction calculant les matères premières nécéssaires pour la fabrication de l'article courant
    # Retourne product lines
    # @api.depends('move_finished_ids.move_line_ids')
    @api.multi
    def action_compute(self):
        results = []
        prod_line_obj = self.env['mrp.production.product.line']

        prod_component_line = self.env['mrp.production.product.component.line']
        prod_accessory_line = self.env['mrp.production.product.accessory.line']

        for production in self:
            # production.show_final_lots = production.product_id.tracking != 'none'
            for line in production.product_lines:
                req = "DELETE FROM mrp_production_product_line WHERE id = (%s)"
                self.env.cr.execute(req, (line.id,))
            for line in production.product_lines1:
                req1 = "DELETE FROM mrp_production_product_component_line WHERE id IN (%s)"
                self.env.cr.execute(req1, (line.id,))
            for line in production.product_lines2:
                req2 = "DELETE FROM mrp_production_product_accessory_line WHERE id IN (%s)"
                self.env.cr.execute(req2, (line.id,))

            res = self.prepare_lines(production)
            results = res['lines_done'] #bom_lines

            # Calcul de la qualité des composants
            # Récupération propriétés
            parent_id = self.product_id.id
            
            qty = self.product_qty
            largeur = self.largeur
            hauteur = self.hauteur
            tms = self.tms
            localdict = {
                'largeur' : largeur,
                'hauteur' : hauteur,
                'tms' : tms,
                'result' : None,
                'style' : self.style,
                'vitre' : self.remplissage_vitre
            }

            # Mise è jour
            if not self.vitre:
                localdict['type_vitre'] = 0
            else : localdict['type_vitre'] = self.vitre.id
            localdict['inter'] = self.intermediaire
            localdict['moust'] = self.moustiquaire
            localdict['div'] = self.division

            if not self.nb_division:
                localdict['nb_div'] = 1.0
            else:
                localdict['nb_div'] = self.nb_division
            
            if not self.type_intermediaire or self.type_intermediaire == 'vert':
                localdict['type_inter'] = 'vert'
            else: localdict['type_inter'] = 'horiz'

            localdict['batis'] = self.batis_id.name

            component = self.env['mrp.component']
            list_components = {}
            for line in results:
                line_id = line[1]['line_id']
                list_id = component.search([('line_id','=',line_id)])
                if list_id:
                    for c in component.browse(list_id).id:
                        total1 = 0.0
                        total2 = 0.0
                        len_total0 = 0.0
                        len_unit0 = 0.0
                        qty_total0 = 0.0
                        #insertion de tous les composants pour l'impression
                        for s in c.sub_component_ids:
                            localdict['Q'] = qty
                            safe_eval(s.python_product_qty,localdict,mode='exec',nocopy=True)
                            product_qty = float(localdict['result'])
                            list_components['production_id'] = production.id
                            list_components['product_qty'] = product_qty
                            localdict['QU'] = list_components['product_qty']

                            safe_eval(s.python_product_qty_total,localdict,mode='exec',nocopy=True)
                            product_qty_total = float(localdict['result'])
                            list_components['product_qty_total'] = product_qty_total
                            
                            qty_total0 = product_qty_total
                            
                            localdict['QT'] = list_components['product_qty_total']
                            total2 = total2 + list_components['product_qty_total']
                            
                            if not line[1]['is_accessory']:
                                list_components['ref'] = c.product_parent_id.partner_ref
                                list_components['name'] = s.name
                                
                                #Calcul de la longueur unitaire du composant
                                safe_eval(s.python_len_unit,localdict,mode='exec',nocopy=True)
                                len_unit = float(localdict['result'])
                                list_components['len_unit'] = len_unit
                               
                                localdict['LU'] = list_components['len_unit']

                                #Calcul de la longueur totale du composant
                                safe_eval(s.python_len_total,localdict,mode='exec',nocopy=True)
                                len_total = float(localdict['result'])
                               
                                list_components['len_total'] = len_total
                                
                                # len_total0 = len_total

                                total1 = total1 + list_components['len_total']
                                LU = list_components['len_unit']
                                LT = list_components['len_total']

                                if list_components['len_total'] != 0.0:
                                    prod_component_line.create(list_components.copy())
                            
                            else:
                                if list_components['product_qty_total'] != 0.0:
                                    list_components['ref'] = c.product_parent_id.name
                                    list_components['name'] = s.name
                                    prod_accessory_line.create(list_components.copy())
                            list_components = {}

                        if not line[1]['is_accessory']:
                            uom = c.product_parent_id.uom_id.name
                            ref = c.product_parent_id.partner_ref
                            len_barre = self.longueur_barre

                            if uom == 'Barre':
                                if ref != 'P50-MB':
                                    line[1]['qty'] = self.get_nb_barres(total1)
                                else:                                    
                                    var = ( LU / 100.0) * LT * qty_total0 / len_barre
                                    line[1]['qty'] = self.round_float(var)
                            else:
                                line[1]['qty'] = (LU * LT * product_qty_total) / 10000.0
                        
                        else: line[1]['qty'] = total2
                        ############################################################################

            # Pour chaque product_line dans production.product_lines
            # reset production dans l'ordre de production
            for line in results:
                if line[1]['qty'] != 0.0:
                    # line['production_id'] = production.id
                    prod_line_obj.create({
                        'product_id' : line[1]['product']['id'],
                        'product_qty' : line[1]['qty'],
                        'production_id' : production.id,
                        'product_uom_id' : line[1]['product']['uom_id']['id'],
                        'name' : line[0]['product_id']['product_tmpl_id']['name']
                        })

            # Mise à jour de l'objet mrp.production
            # prod_obj = self.env['mrp.production']

            # calculate consumption
            if not self.is_calculated and not (self.state == 'done' or self.state == 'cancel'):
                self.count_raw_materials(results)
                self.write({'is_calculated':True})

        _logger.info('results : %s' % (results))
        return results
