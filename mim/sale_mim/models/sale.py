# -*- coding: utf-8 -*-

import time
import datetime
import logging# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from math import ceil as ceil
from odoo import exceptions
from odoo.tools import float_round
from odoo.tools import safe_eval

_logger = logging.getLogger(__name__)


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
    nb_division = fields.Integer(
        string="Nombre division")
    type_intermediaire = fields.Selection(
        string="Type d\'intermédiaire",
        selection=[
            ('vertical', 'Vertical'),
            ('horizontal', 'Horizontal')])

    # need bom_id for computing
    bom_id = fields.Many2one(
        comodel_name='mrp.bom',
        string='Bom ID',
        compute='_get_bom_id',
        store='True',
    )

    @api.multi
    @api.depends('product_id')
    def _get_bom_id(self):
        bom_obj = self.env['mrp.bom']
        for record in self:
            bom_obj_id = bom_obj.search([('product_id', '=', record.product_id.id)])
            if bom_obj_id:
                record.bom_id = bom_obj_id.id

#   Sale_inherit
    @api.depends('largeur', 'hauteur')
    def _get_mesure(self):
        for line in self:
            line.mesure = str(int(line.largeur)) + "  x  " + str(int(line.hauteur))


class SaleOrder(models.Model):
    _inherit = 'sale.order'

#   Make_invoice
    user_id = fields.Many2one(
        string="Salesperson",
        comodel_name="res.users",
        readonly=True,
        default=False)
    # categ_ids = fields.Many2many(
    #     string="Tags",
    #     comodel_name="crm.case.categ")

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

    # # # # # # # # # # # # # # # # # #
    # new features for computing bom  #

    @api.multi
    def _get_nb_barres(self, qty_mm):
        len_barre = 5800
        qty_barres = qty_mm / len_barre
        return ceil(qty_barres)

    @api.multi
    def prepare_lines(self, production, qty, properties=None):
        bom_obj = self.env['mrp.bom']
        uom_obj = self.env['product.uom']
        bom_point = production.bom_id
        # bom_point = production.bom_id
        bom_id = bom_point.id
        if not bom_point:
            bom_id = bom_obj._bom_find(product=production.product_id)
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
        factor = production.product_uom._compute_quantity(
            production.product_uom_qty,
            bom_point.product_uom_id
        ) / bom_point.product_qty
        boms = production.bom_id.bom_explode(
            production.product_id, factor,
            picking_type=production.bom_id.picking_type_id
        )
        return boms

    def quick_sort(self, array):
        array_length = len(array)
        greater = []
        lesser = []
        if (array_length <= 1):
            return array
        else:
            pivot = array[0]
            for element in array[1:]:
                if element[0].product_id.id > pivot[0].product_id.id:
                    greater.append(element)
            for element in array[1:]:
                if element[0].product_id.id <= pivot[0].product_id.id:
                    lesser.append(element)

        return self.quick_sort(lesser) + [pivot] + self.quick_sort(greater)

    def binary_search(self, array, occurence):
        left = 0
        right = len(array) - 1

        while left <= right:
            middle = (left + right) // 2
            if array[middle][0].product_id.id == occurence[0].product_id.id:
                return middle
            elif array[middle][0].product_id.id < occurence[0].product_id.id:
                left = middle + 1
            else:
                right = middle - 1

        return -1

    def action_compute(self, products):
        results = []  # record
        prod_line_obj = self.env['mrp.production.product.line']

        prod_component_line = self.env['mrp.production.product.component.line']
        prod_accessory_line = self.env['mrp.production.product.accessory.line']

        mrp_obj = self.env['mrp.production']
        production = products
        # _logger.info('production_type : %s' % (type(production)))
        products = mrp_obj.search([('product_id', '=', products.product_id.id)], limit=1)

        for pr in products:
            # production.show_final_lots = production.product_id.tracking != 'none'
            for line in pr.product_lines:
                req = "DELETE FROM mrp_production_product_line WHERE id = %s"
                self.env.cr.execute(req, (line.id,))

            for line in pr.product_lines1:
                req1 = "DELETE FROM mrp_production_product_component_line WHERE id = %s"
                self.env.cr.execute(req1, (line.id,))

            for line in pr.product_lines2:
                req2 = "DELETE FROM mrp_production_product_accessory_line WHERE id = %s"
                self.env.cr.execute(req2, (line.id,))

            res = self.prepare_lines(production, production.product_uom_qty)  # alainy n anat bom_line
            results = res['lines_done']  # bom_lines

            # Calcul de la qualité des composants
            # Récupération propriétés
            qty = production.product_uom_qty
            largeur = production.largeur
            hauteur = production.hauteur
            tms = production.tms
            localdict = {
                'largeur': largeur,
                'hauteur': hauteur,
                'tms': tms,
                'result': None,
                # arbitraire
                'style': 'fr',
                'vitre': production.vitre,
            }

            # Mise è jour
            if not production.vitre:
                localdict['type_vitre'] = 0
            else:
                localdict['type_vitre'] = production.vitre.id
            localdict['inter'] = production.intermediaire
            localdict['moust'] = production.moustiquaire
            localdict['div'] = production.division

            # add field of nb_division
            if not production.nb_division:
                localdict['nb_div'] = 1.0
            else:
                localdict['nb_div'] = production.nb_division

            # arbitraire
            if not production.type_intermediaire or production.type_intermediaire == 'vert':
                localdict['type_inter'] = 'vert'
            else:
                localdict['type_inter'] = 'horiz'

            localdict['batis'] = ''

            component = self.env['mrp.component']
            list_components = {}
            for line in results:
                line_id = line[1]['line_id']
                list_id = component.search([('line_id', '=', line_id)])
                if list_id:
                    for c in component.browse(list_id).id:
                        total1 = 0.0
                        total2 = 0.0
                        len_total0 = 0.0
                        len_unit0 = 0.0
                        qty_total0 = 0.0
                        # insertion de tous les composants pour l'impression
                        for s in c.sub_component_ids:
                            localdict['Q'] = qty
                            safe_eval(s.python_product_qty, localdict, mode='exec', nocopy=True)
                            product_qty = float(localdict['result'])
                            list_components['production_id'] = production.id
                            list_components['product_qty'] = product_qty
                            localdict['QU'] = list_components['product_qty']

                            safe_eval(s.python_product_qty_total, localdict, mode='exec', nocopy=True)
                            product_qty_total = float(localdict['result'])
                            list_components['product_qty_total'] = product_qty_total

                            qty_total0 = product_qty_total

                            localdict['QT'] = list_components['product_qty_total']
                            total2 = total2 + list_components['product_qty_total']

                            if not line[1]['is_accessory']:
                                list_components['ref'] = c.product_parent_id.partner_ref
                                list_components['name'] = s.name

                                # Calcul de la longueur unitaire du composant
                                safe_eval(s.python_len_unit, localdict, mode='exec', nocopy=True)
                                len_unit = float(localdict['result'])
                                list_components['len_unit'] = len_unit
                                localdict['LU'] = list_components['len_unit']

                                # Calcul de la longueur totale du composant
                                safe_eval(s.python_len_total, localdict, mode='exec', nocopy=True)
                                len_total = float(localdict['result'])
                                list_components['len_total'] = len_total
                                # len_total0 = len_total

                                total1 = total1 + list_components['len_total']
                                LU = list_components['len_unit']
                                LT = list_components['len_total']

                                # if list_components['len_total'] != 0.0:
                                #     prod_component_line.create(list_components.copy())

                            else:
                                if list_components['product_qty_total'] != 0.0:
                                    list_components['ref'] = c.product_parent_id.name
                                    list_components['name'] = s.name
                                    # prod_accessory_line.create(list_components.copy())
                            list_components = {}

                        if not line[1]['is_accessory']:
                            uom = line[0].product_uom_id.name
                            ref = component.product_parent_id.partner_ref
                            # arbitraire
                            len_barre = 5800

                            if uom == 'Barre':
                                if ref != 'P50-MB':
                                    line[1]['qty'] = self._get_nb_barres(total1)
                                else:
                                    var = (LU / 100.0) * LT * qty_total0 / len_barre
                                    line[1]['qty'] = self.round_float(var)
                            else:
                                line[1]['qty'] = (LU * LT * product_qty_total) / 10000.0

                        else:
                            line[1]['qty'] = total2

        return results

    @api.multi
    def purge(self):
        self.env.cr.execute('delete from sale_count_bom')

    @api.multi
    def count_raw_materials(self, results0, results):

        results = self.quick_sort(results)
        results0 = self.quick_sort(results0)
        for result in results:
            i = self.binary_search(results0, result)
            if i == -1:
                results0.append(result)
                results0 = self.quick_sort(results0)
            else:
                results0[i][1]['qty'] = results0[i][1]['qty'] + result[1]['qty']
        return results0

    @api.multi
    def action_count(self):

        # like gas station counter
        # purge the database before the new user use it
        self.purge()

        sale_order_id = self.id
        sale_order_line_obj = self.env['sale.order.line']
        sale_order_line_obj_ids = sale_order_line_obj.search([('order_id', '=', sale_order_id)])
        # _logger.info('sale_order_line_obj_ids : %s' % (sale_order_line_obj_ids))

        # once we got sale_order_line related to sale_order_id
        # we call action_compute
        # and iterate it with sale_order_line_obj

        results0 = []

        for sale_order_line_obj in sale_order_line_obj_ids:
            results = self.action_compute(sale_order_line_obj)
            results0 = self.count_raw_materials(results0, results)

        raw_materials_obj = self.env['sale.count.bom']
        for result in results0:
            if result[1]['qty'] == 0.0:
                continue
            data = {
                'sale_id': self.id,
                'product_name': result[0].product_id.product_tmpl_id.name,
                'product_id': result[0].product_id.id,
                'product_qty': result[1]['qty'],
                'product_uom_id': result[0].product_uom_id.id,
                'product_uom_name': result[0].product_uom_id.name,
                'product_cat_name': result[0].product_id.product_tmpl_id.categ_id.name
            }
            raw_materials_obj.create(data)

        ctx = dict()
        ctx.update({
            'default_order_id': self.id,
        })
        return {
            'name': _('Consommation bom'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.count.bom',
            'target': 'new',
            'context': ctx,
        }

    # use for benchmark
    def formatSeconds(self, seconds):
        seconds = round(seconds)
        minutes = 0
        hours = 0
        if seconds >= 60:
            minutes = seconds // 60
            seconds = seconds % 60
        if minutes >= 60:
            hours = minutes // 60
            minutes = seconds % 60
        return {'hours': hours, 'minutes': minutes, 'seconds': seconds}

    @api.multi
    def action_count_all(self):
        startTime = time.time()
        self.purge()

        results0 = []
        sale_order_line = self.env['sale.order.line']
        sale_order = self.env['sale.order']
        # sale_order_line_objs = sale_order_objs.search(['&', ('bom_id', '!=', False), ('state', '=', 'sale')], limit=100)
        # sale_order_ids = sale_order.search([('state', '=', 'sale')])

        # for sale_order_id in sale_order_ids:
        #     sale_order_line_ids = sale_order_line.search(['&', ('order_id', '=', sale_order_id.id), ('bom_id', '!=', False)])
        #     # _logger.info('results0: %s' % (results0))
        #     for sale_order_line_id in sale_order_line_ids:
        #         results = self.action_compute(sale_order_line_id)
        #         results0 = self.count_raw_materials(results0, results)
        sale_order_line_ids = sale_order_line.search([('bom_id', '!=', False)])
        for sale_order_line_id in sale_order_line_ids:
            results = self.action_compute(sale_order_line_id)
            results0 = self.count_raw_materials(results0, results)

        raw_materials_obj = self.env['sale.count.bom']
        for result in results0:
            # if result[1]['qty'] == 0.0:
            #     continue
            data = {
                'sale_id': 1,
                'product_name': result[0].product_id.product_tmpl_id.name,
                'product_id': result[0].product_id.id,
                'product_qty': result[1]['qty'],
                'product_uom_id': result[0].product_uom_id.id,
                'product_uom_name': result[0].product_uom_id.name,
                'product_cat_name': result[0].product_id.product_tmpl_id.categ_id.name
            }
            raw_materials_obj.create(data)
        endTime = time.time()
        diff = endTime - startTime
        date = self.formatSeconds(diff)
        _logger.info('temps d\'exécution: %s hours %s minutes %s seconds' % (date['hours'], date['minutes'], date['seconds']))
