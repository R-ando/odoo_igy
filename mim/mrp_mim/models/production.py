# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.tools.safe_eval import safe_eval
import logging
_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    largeur = fields.Float(
        string="Largeur")
    hauteur = fields.Float(
        string="Hauteur")
    nbr_barre = fields.Float(
        string="Nombre total de barres")
    
    #Product line for article and accessory
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
    
    #Ligne des produits pour la fabrication d'un article
    product_lines = fields.One2many(
        string="Scheduled goods",
        comodel_name="mrp.production.product.line",
        inverse_name="production_id",
        readonly=True,
        states={'confirmed': [('readonly', False)]})
    
    partner_name = fields.Char(
        string="Nom du client",
        compute='_get_partner_name')

    #Test si l'article a été consumé ou produit
    @api.multi
    def test_if_product(self):
        # Retourne True or False
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
    
    @api.depends('partner_id')
    def _get_partner_name(self):
        for production in self:
            production.partner_name = production.partner_id.name

    
    @api.multi
    def set_state_to_verified(self):
        self.write({
            'state' : 'verified'
            })

    @api.multi
    def set_state_to_confirmed(self):
        self.write({
            'state' : 'confirmed'
            })

    @api.multi
    def set_state_to_validated(self):
        self.write({
            'state' : 'validated'
            })
    @api.multi
    def moves_ready(self):
        self.write({
            'state' : 'progress'
            })

    #Fontion calculant les données de product lines
    @api.multi
    def action_compute_stock_move(self):
        results = []

        for production in self:
            res = self.prepare_lines(production)
            results = res['lines_done']

            #Calcul de la qualité des composants
            #Récupération propriétés
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
                'vitre' : self.vitre,
            }

            #Mise è jour
            if not self.vitre:
                localdict['type_vitre'] = 0
            else : localdict['type_vitre'] = self.vitre.id
            localdict['inter'] = self.intermediaire
            localdict['moust'] = self.moustiquaire
            localdict['div'] = self.division

            if not self.nb_division:
                localdict['nb_div'] = 1.0
            else: localdict['nb_div'] = self.nb_division

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
                                #len_total0 = len_total

                                total1 = total1 + list_components['len_total']
                                LU = list_components['len_unit']
                                LT = list_components['len_total']

                                # if list_components['len_total'] != 0.0:
                                #     _logger.info("\n*****list_components = %s*****\n" % list_components)                            
                            else:
                                if list_components['product_qty_total'] != 0.0:
                                    list_components['ref'] = c.product_parent_id.name
                                    list_components['name'] = s.name
                            list_components = {}

                        if not line[1]['is_accessory']:
                            uom = line[0].product_uom_id.name
                            ref = component.product_parent_id.partner_ref
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

        return res['boms_done'], results

    #Surcharge de la fonction _generate_moves
    def _generate_moves(self):
        for production in self:
            production._generate_finished_moves()
            # factor = production.product_uom_id._compute_quantity(production.product_qty,production.bom_id.product_uom_id) / production.bom_id.product_qty
            boms,lines = production.action_compute_stock_move() #Vérifier la valeur de retou
            production._generate_raw_moves(lines) #Création de stock.move avec la quantité calculer
            # Check for all draft moves whether they are mto or not
            production._adjust_procure_method()
            production.move_raw_ids._action_confirm()
        return True

    #Surcharge de la fonction _generate_raw_moves
    def _generate_raw_moves(self,exploded_lines):
        self.ensure_one()
        moves = self.env['stock.move']
        for bom_line, line_data in exploded_lines:
            move = self._generate_raw_move(bom_line,line_data)
            if move != None:
                moves += move
        return moves

    #Surcharge de la fonction _generate_raw_move
    def _generate_raw_move(self,bom_line,line_data):
        quantity = line_data['qty']
        # alt_op needed for the case when you explode phantom bom and all the lines will be consumed in the operation given by the parent bom line
        alt_op = line_data['parent_line'] and line_data['parent_line'].operation_id.id or False
        if bom_line.child_bom_id and bom_line.child_bom_id.type == 'phantom':
            return self.env['stock.move']
        if bom_line.product_id.type not in ['product', 'consu']:
            return self.env['stock.move']
        if self.routing_id:
            routing = self.routing_id
        else:
            routing = self.bom_id.routing_id
        if routing and routing.location_id:
            source_location = routing.location_id
        else:
            source_location = self.location_src_id

        if quantity != 0.0:
            original_quantity = (self.product_qty - self.qty_produced) or 1.0
            _logger.info("\n*****original_quantity = %s*****\n" % original_quantity)
            data = {
            'sequence': bom_line.sequence,
            'name': self.name,
            'date': self.date_planned_start,
            'date_expected': self.date_planned_start,
            'bom_line_id': bom_line.id,
            'product_id': bom_line.product_id.id,
            'product_uom_qty': quantity,
            'product_uom': bom_line.product_uom_id.id,
            'location_id': source_location.id,
            'location_dest_id': self.product_id.property_stock_production.id,
            'raw_material_production_id': self.id,
            'company_id': self.company_id.id,
            'operation_id': bom_line.operation_id.id or alt_op,
            'price_unit': bom_line.product_id.standard_price,
            'procure_method': 'make_to_stock',
            'origin': self.name,
            'warehouse_id': source_location.get_warehouse().id,
            'group_id': self.procurement_group_id.id,
            'propagate': self.propagate,
            'unit_factor': quantity / original_quantity,
            }
            return self.env['stock.move'].create(data)

    #Fonction d'arrondissement du n barre
    def round_float(self,qty):
        s = str(qty)
        t = s.split('.')
        dec = 0
        if int(t[1]) > 0:
            dec = 1
        res = int(t[0]) + dec
        return res

    #Fonction rrécupérant le nb de barre
    @api.multi
    def get_nb_barres(self,qty_mm):
        len_barre = self.longueur_barre #(longeur de barre en mm)
        qty_barres = qty_mm / len_barre
        return self.round_float(qty_barres)
    

    #Test si move_raw_ids est prêt ou non
    @api.multi
    def test_ready(self):
        res = True
        for production in self:
            if production.move_raw_ids:  #and not production.ready_production:
                res = False

        return res
    
    #Forcer la production de l'article
    @api.multi
    def force_production(self):
        move_obj = self.env['stock.move']
        for order in self:
            move_obj.force_assign([x.id for x in order.move_raw_ids])
            prod_obj = self.env['mrp.production']
            if prod_obj.test_ready([order.id]):
                prod_obj.moves_ready()

        return True

    #Rendre disponible le stock.move lié à l'ordre de fabrication
    @api.multi
    def set_move_available(self,production_id):
        production = self.browse(production_id)
        if production.move_prod_id.id:
            move_id = self.env['stock.move'].browse(production.move_prod_id.id)
            move_id.force_assign()
        else:
            raise exceptions.ValidationError("Cette ordre de fabrication n'est lié à aucun mouvement de stock")

        return True

    # Verifie si l'état de stock.move n'est pas en contre-mesure
    @api.multi
    def action_verified(self):
        move_obj = self.env['stock.move']
        for prod in self:
            state_move = move_obj.browse(prod.move_prod_id.id).state
            if state_move != 'contre_mesure':
                raise exceptions.ValidationError("Le mouvement lié à cet ordre de fabrication n'est pas en contre-mesure")
            if prod.hauteur == 0.0 or prod.largeur == 0.0:
                raise exceptions.ValidationError("Les contre-mesures ne doivent pas être vides")
        self.write({
            'state' : 'verified'
            })
    
    #Retourne BOM structure
    @api.multi
    def prepare_lines(self,production):
        bom_obj = self.env['mrp.bom']
        bom_point = production.bom_id
        bom_id = production.bom_id.id
        if not bom_point:
            bom_id = bom_obj._bom_find(product=production.product_id)
            if bom_id:
                bom_point = bom_obj.browse(bom_id)
                routing_id = bom_point.routing_id.id or False
                self.write([production.id],{
                    'bom_id':bom_id,
                    'routing_id' : routing_id,
                    })
        if not bom_id:
            raise exceptions.ValidationError("Ne peut pas trouver le bilan de ce matériel")
        #get components from BOM structure
        factor = production.product_uom_id._compute_quantity(production.product_qty,bom_point.product_uom_id) / bom_point.product_qty
        boms = production.bom_id.bom_explode(production.product_id,factor,picking_type=production.bom_id.picking_type_id)
        return  boms


    #Fonction calculant les matères premières nécéssaires pour la fabrication de l'article courant
    #Retourne une liste contenant tous les infos de calcul
    @api.multi
    def action_compute(self):
        results = []

        prod_line_obj = self.env['mrp.production.product.line']
        prod_component_line = self.env['mrp.production.product.component.line']
        prod_accessory_line = self.env['mrp.production.product.accessory.line']

        for production in self:

            #Suppression pour éviter toute duplication dans la base de données
            for line in production.product_lines:
                # req = "DELETE FROM mrp_production_product_line WHERE id IN (%s)"
                line.unlink()
                # self.env.cr.execute(req, (line.id,))

            for line in production.product_lines1:
                # req1 = "DELETE FROM mrp_production_product_component_line WHERE id IN (%s)"
                line.unlink()
                # self.env.cr.execute(req1, (line.id,))

            for line in production.product_lines2:
                # req2 = "DELETE FROM mrp_production_product_accessory_line WHERE id IN (%s)"
                line.unlink()
                # self.env.cr.execute(req2, (line.id,))

            #Récupération des bom_lines par prepare_lines
            res = self.prepare_lines(production)
            results = res['lines_done'] #bom_lines

            #Calcul de la qualité des composants
            #Récupération propriétés
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
                'vitre' : self.vitre,
            }

            #Mise è jour
            if not self.vitre:
                localdict['type_vitre'] = 0
            else : localdict['type_vitre'] = self.vitre.id
            localdict['inter'] = self.intermediaire
            localdict['moust'] = self.moustiquaire
            localdict['div'] = self.division

            if not self.nb_division:
                localdict['nb_div'] = 1.0
            else: localdict['nb_div'] = self.nb_division

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
                                #len_total0 = len_total

                                total1 = total1 + list_components['len_total']
                                LU = list_components['len_unit']
                                LT = list_components['len_total']

                                if list_components['len_total'] != 0.0:
                                    _logger.info("\n*****list_components = %s*****\n" % list_components)
                                    prod_component_line.create(list_components.copy())
                            
                            else:
                                if list_components['product_qty_total'] != 0.0:
                                    list_components['ref'] = c.product_parent_id.name
                                    list_components['name'] = s.name
                                    prod_accessory_line.create(list_components.copy())
                            list_components = {}

                        if not line[1]['is_accessory']:
                            uom = line[0].product_uom_id.name
                            ref = component.product_parent_id.partner_ref
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

            #Pour chaque product_line dans production.product_lines
            #reset production dans l'ordre de production
            for line in results:
                if line[1]['qty'] != 0.0:
                    prod_line_obj.create({
                        'product_id' : line[1]['product'].id,
                        'product_qty' : line[1]['qty'],
                        'production_id' : production.id,
                        'product_uom_id' : line[0].product_uom_id.id,
                        'name' : line[0]['product_id']['product_tmpl_id']['name'],
                        'line_id' : line[1]['line_id'],
                        'is_accessory': line[1]['is_accessory'],
                        })

            #Mise à jour de l'objet mrp.production
            self.write({'is_calculated':True})

        return results

