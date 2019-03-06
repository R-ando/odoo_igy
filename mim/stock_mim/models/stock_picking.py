# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT,DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)
class StockPicking(models.Model):
    _inherit = 'stock.picking'


    @api.one
    def compute_moves(self):
        # request="SELECT * FROM stock_move WHERE origin NOT LIKE '\%MO\%' AND picking_type_id = 2 AND state LIKE '\%contre\%'"
        # self.env.cr.execute(request)
        # res = self.env.cr.fetchall()
        # moves = self.env['stock.move'].search([('origin', 'not like', 'MO'), ('picking_type_id', '=', 2), ('state', 'like', 'contre')]).mapped('name')
        moves = self.env['stock.move'].search([('name', 'not like', 'MO')]).mapped('name')
        return moves
        # move_i = moves
        # print("=============================",move_ids,"=====================")

    # @api.multi
    # def _get_domain(self):
    #     model = self.env['ir.model.data'].search([('name', '=', 'mrp_bom')])
    #     product_list = [x for x in model.mapped('product_id')]
    #     return product_list

# bon de livraison 1
    motivation = fields.Text(
        string="Motivation")
    date_changed = fields.Boolean(
        string=u"Date changée",
        default=False)
    # product_list = fields.Many2one('mrp.bom', store=True, compute=_get_domain)
    # move_i = fields.One2many('stock.move','picking_id', string="moves",copy=True, domain="compute_moves")
    # move_lines = fields.One2many('stock.move', 'picking_id', string="Stock Moves", copy=True)

# stock_mim_final/stock_move_split
    state = fields.Selection(
        string="Status",
        selection=[
            ('draft', 'Draft'),
            ('waiting', 'Waiting Another Operation'),
            ('confirmed', 'Waiting'),
            ('contre_mesure', 'Contre mesure'),
            ('flowsheeting', u'Fiche de Débit'),
            ('assigned', 'Ready'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
        ],
        compute='_compute_state',
        copy=False, index=True, readonly=True, store=True,
        track_visibility='onchange',
        help=" * Draft: not confirmed yet and will not be scheduled until confirmed.\n"
             " * Waiting Another Operation: waiting for another move to proceed before it becomes automatically available (e.g. in Make-To-Order flows).\n"
             " * Waiting: if it is not ready to be sent because the required products could not be reserved.\n"
             " * Ready: products are reserved and ready to be sent. If the shipping policy is 'As soon as possible' this happens as soon as anything is reserved.\n"
             " * Done: has been processed, can't be modified or cancelled anymore.\n"
             " * Cancelled: has been cancelled, can't be confirmed anymore."

    )

# stock_mrp
    mo_created = fields.Boolean(
        string="Ordre de fabrication créé",
        compute="_get_mo_created")
        #store=False)
    late_production = fields.Float(
        string="Retard de production (Jours)",
        compute='_get_late')
    production_date = fields.Datetime(
        string="Date de fin de production")
    late_delivery = fields.Float(
        string="Retard de livraison (Jours)")
    delivery_date = fields.Datetime(
        string="Date de fin de livraison")
    is_old_picking_assigned = fields.Boolean(
        string="Ancien BL disponible",
        default=False)
    is_old_picking_done = fields.Boolean(
        string="Ancien BL terminé",
        default=False)
    mo_created_copy = fields.Boolean(
        string="Ordre de fabrication créé ?")

# stock_state
    confirmed = fields.Char(
        string=u"Attente de disponibilité")
    contre_mesure = fields.Char(
        string="Contre Mesure")
    fiche_debit = fields.Char(
        string=u"Fiche de débit")
    assigned = fields.Char(
        string="Disponible")
    done = fields.Char(
        string=u"Terminé")
    total = fields.Char(
        string="Total")



    @api.multi
    def confirm_configs_mo(self):
        ctx = dict()
        ctx.update({
            'default_picking_id': self.id,
            'default_date_planned': self.date,
            })
        return {
            'name' : u'Veuillez entrer la date prévue',
            'type' : 'ir.actions.act_window',
            'view_type' : 'form',
            'view_mode' : 'form',
            'res_model' : 'mrp.configuration',
            'nodestroy' : True,
            'target' : 'new',
            'context' : ctx,
        }

    @api.multi
    def view_all_mo(self):
        mod_obj = self.env['ir.model.data']
        act_obj = self.env['ir.actions.act_window']
        result = mod_obj.get_object_reference('mrp','mrp_production_action')
        # _logger.info("\n*****result = %s*****\n" % result)
        ident = result and result[1] or False
        result = act_obj.read([ident])
        mo_ids = [p.id_mo for p in self.move_lines if p.id_mo]
        if len(mo_ids) < 1:
            return{}
        else:
            if len(mo_ids) > 1:
                res_view = mod_obj.get_object_reference('mrp','mrp_production_tree_view')
                result.append("[('id','in',["+','.join(map(str,mo_ids))+"])]") #domain
                return{
                    "name":_("MO Tree"),
                    'domain' : result[0],
                    'view_mode':'tree,form',
                    'view_type':'form',
                    "res_model":"mrp.production",
                    "type":"ir.actions.act_window",
                    "target":"current",
                }
            else:
                res = mod_obj.get_object_reference('mrp','mrp_production_form_view')
                result.append((res and res[1] or False)) #views
                result.append(mo_ids and mo_ids[0] or False) #res_id
                return {
                    'type' : 'ir.actions.act_window',
                    'name' : 'Ordre de fabrication',
                    'res_model' : 'mrp.production',
                    'res_id' : result[1],
                    'view_type' : 'form',
                    'view_mode' : 'form',
                    'view_id' : result[0],
                    'target' : 'current',
                    'nodestroy' : True,
                }


    @api.depends('move_type','move_lines.state','move_lines.picking_id')
    @api.multi
    def _state_get_new(self):
        res = {}
        for pick in self:
            if (not pick.move_lines) or any([x.state == 'draft' for x in pick.move_lines]):
                res[pick.id] = 'draft'
                continue
            if all([x.state == 'cancel' for x in pick.move_lines]):
                res[pick.id] = 'cancel'
                continue
            if all([x.state in ('cancel','done') for x in pick.move_lines]):
                res[pick.id] = 'done'
                continue

            #Prise en considération des états contre_mesure et fiche de débit
            if all(x.state in ('flowsheeting','contre_mesure') for x in pick.move_lines):
                res[pick.id] = 'confirmed'
                continue

            order = {'confirmed':0, 'waiting':1, 'assigned':2}
            order_inv = {0:'confirmed', 1:'waiting', 2:'assigned'}

          #Ignorer les états contre_mesure et fiche de debit
            lst = [order[x.state] for x in pick.move_lines if x.state not in ('cancel','done','contre_mesure','flowsheeting')]
            if lst == []:
                continue

            if pick.move_type == 'one':
                res[pick.id] = order_inv[min(lst)]
            else:
                res[pick.id] = order_inv[max(lst)]
                if not all(x == 2 for x in lst) or any(x.state in ('contre_mesure','flowsheeting') for x in pick.move_lines):
                    if any(x == 2 for x in lst):
                        res[pick.id] = 'partially_available'
                    else:
                        # Si tout mvt n'est assigné, verifier si un article est partiellement dispo
                        for move in pick.move_lines:
                            if move.state == 'partially_available':
                                res[pick.id] = 'partially_available'
                                break
        return res

    # @api.onchange('move_lines.product_id')
    # def _onchange_move_lines(self):
    #     variant_ids_list = []
    #     move = self.env['stock.move']
    #     if move._context.get('group_id'):
    #         group_id = move.env["procurement.group"].browse(self._context.get('group_id'))
    #         for variant_id in group_id.product_variant_ids:
    #             if variant_id.rule_id == 1 :
    #                 variant_ids_list.append(variant_id.id)
    #     return {
    #         'domain':{
    #             'move_lines.product_id':[[('id','in',variant_ids_list)]]
    #         }
    #     }

    #Fct obtenir list des picking en stock
    @api.multi
    def _get_pickings(self):
        res = set()
        for move in self:
            if move.picking_id:
                res.add(move.picking_id.id)
        return list(res)

    # Fonction calculant le retard de la production en jours
    @api.multi
    def _get_late(self):
        res = {}
        fmt_datetime = DEFAULT_SERVER_DATETIME_FORMAT
        fmt_date = DEFAULT_SERVER_DATE_FORMAT
        for pick in self:
            if not pick.date:
                res[pick.id] = False
                continue
            if pick.is_old_picking_assigned and pick.name == 'late_production':
                res[pick.id] = False
                continue
            if pick.is_old_picking_done and pick.name == 'late_delivery':
                res[pick.id] = False
                continue

            date_delivery = str(pick.date)
            date_reference = str(datetime.now().strftime(fmt_datetime))
            if pick.name == 'late_production' and pick.production_date:
                date_reference = str(pick.production_date)
            if pick.name == 'late_delivery' and pick.delivery_date:
                date_reference = str(pick.delivery_date)
            d1 = datetime.strptime(str(datetime.strptime(date_reference, fmt_datetime).date()), fmt_date)
            d2 = datetime.strptime(str(datetime.strptime(date_delivery, fmt_datetime).date()), fmt_date)
            diff_date = d1 - d2
            days = diff_date.days
            res[pick.id] = days

        return res

    # @api.multi
    def _get_mo_created(self):
        res = {}
        for pick in self:
            res[pick.id] = False
            if any(move.id_mo for move in pick.move_lines):
                res[pick.id] = True
            pick.write({'mo_created_copy' : res[pick.id]})

        return res

    #Classe pour la configuration de la date
class StockMrp(models.Model):
    _name = 'mrp.configuration'
    # _description = 'Description'

    @api.multi
    def _get_picking_id(self):
        if context is None: context = {}
        return context.get('picking_id', False)
        # return self.env.context.get('picking_id',False)

    @api.multi
    def _get_date_planned(self):
        if context is None: context = {}
        return context.get('date_planned', False)
        # return self.env.context.get('date_planned',False)

    picking_id = fields.Integer(
        string='Id current picking line',
        default='_get_picking_id',
    )

    date_planned = fields.Datetime(
        string='Date plannifiée',
        required=True,
        default='_get_date_planned',
    )

    @api.multi
    def update_moves_data(self):
        picking_obj = self.env['stock.picking']
        picking_id = self.picking_id

        new_date_planned = self.date_planned
        for pick in picking_obj.browse([picking_id]):
            for move in pick.move_lines:
                stock_move_id = move.id

                #Création de l'ordre de fabrication
                move_data = self.env['stock.move'].browse(stock_move_id)
                self.env.cr.execute("""SELECT mrp_bom.id from mrp_bom INNER JOIN
                    product_product ON mrp_bom.product_id = product_product.id WHERE
                    product_product.id = {0} """.format(move_data.product_id.id) )
                res_req = self.env.cr.dictfetchone()

                if res_req:
                    bom_id = res_req['id']
                else:
                    bom_id = False

                #Récupération dans la ligne de commande
                if move_data and move_data.sale_line_id:
                    sale_line_id = move_data.sale_line_id
                else:
                    raise exceptions.ValidationError("Un mouvement n'est pas lié à aucun bon de commande")
                #Création de dictionnaire pour l'enregistrement
                vals = {
                    'origin' : move_data.origin,#
                    'product_id' : move_data.product_id.id,#
                    'product_qty' : move_data.product_qty,#
                    'product_uom_id' : move_data.product_uom.id,#
                    'location_src_id' : move_data.location_id.id,#
                    'location_dest_id' : move_data.location_dest_id.id,#
                    'bom_id' : bom_id,#
                    'date_planned' : new_date_planned,# date_planned_start, date_planned_finnished,*
                    'move_prod_id' : move_data.id,#a chercher 'stock.move'
                    'company_id' : move_data.company_id.id,#
                    'largeur' : move_data.largeur,#*
                    'hauteur' : move_data.hauteur,#*
                    'is_printable' : move_data.is_printable,#*
                    'description' : move_data.name,#
                    'partner_id' : move_data.picking_id.partner_id.id,#*

                    #mim wizard
                    'dimension' : sale_line_id.dimension,#*
                    'vitre' : sale_line_id.vitre.id,#*
                    'type_vitre' : sale_line_id.type_vitre,#*
                    'decoratif' : sale_line_id.decoratif.id,#*
                    'poigne' : sale_line_id.poigne.id,#*
                    'nb_poigne' : sale_line_id.nb_poigne,#*
                    'serr' : sale_line_id.serr.id,#*
                    'nb_serr' : sale_line_id.nb_serr,#*
                    'oscillo_battant' : sale_line_id.oscillo_battant,#*
                    'va_et_vient' : sale_line_id.va_et_vient,#*
                    'butoir' : sale_line_id.butoir,#*
                    'remplissage_vitre' : sale_line_id.remplissage_vitre,#*
                    'type_fixe' : sale_line_id.type_fixe,#*
                    'inegalite' : sale_line_id.inegalite,#*
                    'cintre' : sale_line_id.cintre,#*
                    'triangle' : sale_line_id.triangle,#*
                    'division' : sale_line_id.division,#*
                    'nb_division' : sale_line_id.nb_division,#*
                    'laque' : sale_line_id.laque,#*
                    'moustiquaire' : sale_line_id.moustiquaire,#*
                    'tms' : sale_line_id.tms,#*
                    'type_moustiquaire' : sale_line_id.type_moustiquaire,#*
                    'intermediaire' : sale_line_id.intermediaire,#*
                }
                production_obj = self.env['mrp.production']
                # stock_move_obj = self.env['stock.move']
                mo = production_obj.create(vals)

                val = {
                    'id_mo' : mo.id,
                    'user_id' : self.env.uid,
                    'is_mo_created' : True,
                }
                move_data.write(val)#stock_move (have a field id_mo which is an integer)
        return True
        # return {
        #    'type' : 'ir.actions.client',
        #    'tag' : 'reload',
        # }




    @api.multi
    def create_mo_s(self):
       self.update_moves_data()




