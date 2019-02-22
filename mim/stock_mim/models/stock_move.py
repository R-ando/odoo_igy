# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import logging
_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = 'stock.move'

    user_id = fields.Many2one(
        string="Créateur de l'Ordre de Fabrication",
        comodel_name="res.users")
# mrp
    id_mo = fields.Integer(
        string="Id manufacturing order")
    is_mo_created = fields.Boolean(
        string="Ordre de fabrication créé",
        default=False)
    is_printable = fields.Boolean(
        string="Fiche de débit standard",
        default=False)
    in_mrp_valider_group = fields.Boolean(
        string='Utilisateur courant dans le groupe "Valider fiche de débit"')

    largeur = fields.Float(
        string="Largeur")
    hauteur = fields.Float(
        string="Hauteur")

# stock_mim_final
    state = fields.Selection(
        string="Status",
        selection=[
            ('draft', 'New'), ('cancel', 'Cancelled'),
            ('waiting', 'Waiting Another Move'),
            ('confirmed', 'Waiting Availability'),
            ('contre_mesure', 'Contre mesure'),
            ('flowsheeting', u'Fiche de Débit'),
            ('partially_available', 'Partially Available'),
            ('assigned', 'Available'),
            ('done', 'Done')
        ],
        copy=False, default='draft', index=True, readonly=True,
        help="* New: When the stock move is created and not yet confirmed.\n"
             "* Waiting Another Move: This state can be seen when a move is waiting for another one, for example in a chained flow.\n"
             "* Waiting Availability: This state is reached when the procurement resolution is not straight forward. It may need the scheduler to run, a component to be manufactured...\n"
             "* Available: When products are reserved, it is set to \'Available\'.\n"
             "* Done: When the shipment is processed, the state is \'Done\'."
    )

# stock_mrp
    name = fields.Text(
        string="Description")

    # Surcharge write pour stock.move
    @api.multi
    def write(self,vals):
        if vals.get('largeur') or vals.get('hauteur') or vals.get('is_printable'):
            mo_vals = {
                'largeur' : self.largeur,
                'hauteur' : self.hauteur,
                'is_printable' : self.is_printable,
            }
            mrp_prod_id = self.id_mo
            mrp_prod_obj = self.env['mrp.production'].browse(mrp_prod_id)
            mrp_prod_obj.write(mo_vals)

        #Mise à jour de la date de production
        pick_obj = self.env['stock.picking']
        date_now = datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        if vals.get('state'):
            for move in self:
                pick = pick_obj.browse(move.picking_id.id)
                if all(x.state == 'assigned' for x in pick.move_lines) and not pick.production_date:
                    pick.write({'production_date' : date_now })
                if all(x.state == 'done' for x in pick.move_lines) and not pick.delivery_date:
                    pick.write({'delivery_date' : date_now})

        return super(StockMove,self).write(vals)

    # Fonction changeant les etats
    @api.multi
    def change_state_to_contre_mesure(self):

        self.write({
            'state' : 'contre_mesure',
            'largeur' : self.largeur,
            'hauteur' : self.hauteur,
            # 'is_printable' : True,
            })
        return True

    @api.multi
    def change_state_to_fiche_debit(self):
        self.write({
            'state' : 'flowsheeting',
            #'is_printable' : True,
            })
        return True

    @api.multi
    def change_state_to_waiting(self):
        self.write({
            'state' : 'confirmed',
            })
        return True
    
    #Fct voir l'ordre de fabrication
    @api.multi
    def act_view_mo(self):
        id_mo = self.id_mo
        view_ref = self.env['ir.model.data'].get_object_reference('mrp', 'mrp_production_form_view')
        view_id = view_ref and view_ref[1] or False
        return {
            'type' : 'ir.actions.act_window',
            'name' : 'Ordre de Fabrication',
            'res_model' : 'mrp.production',
            'res_id' : id_mo,
            'view_type' : 'form',
            'view_mode' : 'form',
            'view_id' : view_id,
            'target' : 'current',
            'nodestroy' : True,
        }

    
    #Fct confirmation mo et fiche de debit
    @api.multi
    def confirm_config_mo(self):
        ctx = dict()
        ctx.update({
            'default_is_printable' : self.is_printable,
            'default_stock_move_id' : self.id
            })

        return {
            'name' : u'Veuillez cocher la case si la fiche de debit est une fiche standard',
            'type' : 'ir.actions.act_window',
            'view_type' : 'form',
            'view_mode' : 'form',
            'res_model' : 'choice.configuration',
            'nodestroy' : True,
            'target' : 'new',
            'context' : ctx,
        }


#Classe pour le choix de configuration
class ChoiceConfiguration(models.Model):
    def _get_stock_move_id(self):
        return self.env.context.get('stock_move_id',False)
    
    def _get_is_printable(self):
        return self.env.context.get('is_printable', False)

    _name = 'choice.configuration'

    is_printable = fields.Boolean(
        string='La fiche de débit est une fiche standard',
        default=_get_is_printable 
    )
    stock_move_id = fields.Integer(
        string='Id courant du stock move line',
        default=_get_stock_move_id
    )

    @api.multi
    def update_stock_move(self):
        stock_move_id = self.stock_move_id
        stock_move = self.env['stock.move'].browse(stock_move_id)
        _logger.info("\n*****stock_move = %s*****\n" % stock_move)
        self.env.cr.execute('''SELECT mrp_bom.id FROM mrp_bom INNER JOIN product_product 
            ON mrp_bom.product_id = product_product.id WHERE product_product.id={0}'''
            .format(stock_move.product_id.id))
        
        res_req = self.env.cr.dictfetchone()
        
        largeur = stock_move.largeur
        hauteur = stock_move.hauteur

        if (largeur != 0.0 and hauteur != 0.0):
            if res_req:
                bom_id = res_req['id']

                #Recupération sale_line (ligne de commande)
                if stock_move and stock_move.sale_line_id:
                    sale_line_id = stock_move.sale_line_id
                else:
                    raise exceptions.ValidationError("Ce mouvement n'est lié à aucun bon de commande")
                
                vals = {
                    'origin': stock_move.origin,
                    'product_id': stock_move.product_id.id,
                    'product_qty': stock_move.product_qty,
                    'product_uom_id': stock_move.product_uom.id,
                    # 'product_uos_qty': stock_move.product_uos and stock_move.product_uos_qty or False,
                    # 'product_uos': stock_move.product_uos and stock_move.product_uos.id or False,
                    'location_src_id': stock_move.location_id.id,
                    'location_dest_id': stock_move.location_dest_id.id,
                    'bom_id': bom_id,
                    'date_planned': stock_move.date_expected,
                    'move_prod_id': stock_move.id,
                    'company_id': stock_move.company_id.id,
                    'largeur': stock_move.largeur,
                    'hauteur': stock_move.hauteur,
                    'is_printable':self.is_printable,
                    'description':stock_move.name,
                    'partner_id':stock_move.partner_id.id,
                    
                    #mim wizard
                    'dimension':sale_line_id.dimension,
                    'vitre':sale_line_id.vitre.id,
                    'type_vitre':sale_line_id.type_vitre,
                    'decoratif' :sale_line_id.decoratif.id, 
                    'poigne' :sale_line_id.poigne.id,
                    'nb_poigne':sale_line_id.nb_poigne,
                    'serr' :sale_line_id.serr.id,
                    'nb_serr':sale_line_id.nb_serr,
                    'oscillo_battant':sale_line_id.oscillo_battant,
                    'va_et_vient':sale_line_id.va_et_vient,
                    'butoir':sale_line_id.butoir,
                    'remplissage_vitre':sale_line_id.remplissage_vitre,
                    'type_fixe':sale_line_id.type_fixe,
                    'inegalite':sale_line_id.inegalite,
                    'cintre':sale_line_id.cintre,
                    'triangle':sale_line_id.triangle,
                    'division':sale_line_id.division,
                    'nb_division':sale_line_id.nb_division,
                    'laque':sale_line_id.laque,
                    'moustiquaire':sale_line_id.moustiquaire,
                    'tms':sale_line_id.tms,
                    'type_moustiquaire':sale_line_id.type_moustiquaire,
                    'intermediaire':sale_line_id.intermediaire,
                }
                # _logger.info("\n*****vals = %s*****\n" % vals)
                production_obj = self.env['mrp.production']
                id_mo = production_obj.create(vals)
                
                val = {
                    'id_mo' : id_mo,
                    'user_id' : self.env.uid,
                    'is_mo_created' : True,
                }
                stock_move.write(val)
            
            else:
                raise exceptions.ValidationError('Il n\'existe pas de nomenclature pour cet article')
        else:
            raise exceptions.ValidationError('Veuillez saisir les contre-mesures avant de valider')    

        return True

