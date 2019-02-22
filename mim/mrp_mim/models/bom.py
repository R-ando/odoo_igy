# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.tools import float_round

# Classe nomenclature des articles
class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    #Surcharge de la fonction explode
    @api.multi
    def bom_explode(self, product, quantity, picking_type=False):
        """
            Explodes the BoM and creates two lists with all the information you need: bom_done and line_done
            Quantity describes the number of times you need the BoM: so the quantity divided by the number created by the BoM
            and converted into its UoM
        """
        from collections import defaultdict

        graph = defaultdict(list)
        V = set()

        def check_cycle(v, visited, recStack, graph):
            visited[v] = True
            recStack[v] = True
            for neighbour in graph[v]:
                if visited[neighbour] == False:
                    if check_cycle(neighbour, visited, recStack, graph) == True:
                        return True
                elif recStack[neighbour] == True:
                    return True
            recStack[v] = False
            return False

        boms_done = [(self, {'qty': quantity, 'product': product, 'original_qty': quantity, 'parent_line': False})]
        lines_done = []
        V |= set([product.product_tmpl_id.id])

        bom_lines = [(bom_line, product, quantity, False) for bom_line in self.bom_line_ids]
        for bom_line in self.bom_line_ids:
            V |= set([bom_line.product_id.product_tmpl_id.id])
            graph[product.product_tmpl_id.id].append(bom_line.product_id.product_tmpl_id.id)
        while bom_lines:
            current_line, current_product, current_qty, parent_line = bom_lines[0]
            bom_lines = bom_lines[1:]

            if current_line._skip_bom_line(current_product):
                continue

            line_quantity = current_qty * current_line.product_qty
            bom = self._bom_find(product=current_line.product_id, picking_type=picking_type or self.picking_type_id, company_id=self.company_id.id)
            if bom.type == 'phantom':
                converted_line_quantity = current_line.product_uom_id._compute_quantity(line_quantity / bom.product_qty, bom.product_uom_id)
                bom_lines = [(line, current_line.product_id, converted_line_quantity, current_line) for line in bom.bom_line_ids] + bom_lines
                for bom_line in bom.bom_line_ids:
                    graph[current_line.product_id.product_tmpl_id.id].append(bom_line.product_id.product_tmpl_id.id)
                    if bom_line.product_id.product_tmpl_id.id in V and check_cycle(bom_line.product_id.product_tmpl_id.id, {key: False for  key in V}, {key: False for  key in V}, graph):
                        raise exceptions.UserError(('Recursion error!  A product with a Bill of Material should not have itself in its BoM or child BoMs!'))
                    V |= set([bom_line.product_id.product_tmpl_id.id])
                boms_done.append((bom, {
                    'qty': converted_line_quantity, 
                    'product': current_product, 
                    'original_qty': quantity, 
                    'parent_line': current_line,
                }))
            else:
                # We round up here because the user expects that if he has to consume a little more, the whole UOM unit
                # should be consumed.
                rounding = current_line.product_uom_id.rounding
                line_quantity = float_round(line_quantity, precision_rounding=rounding, rounding_method='UP')
                lines_done.append((current_line, 
                    {'qty': line_quantity, 
                    'product': current_product, 
                    'original_qty': quantity, 
                    'parent_line': parent_line,

                    #Ajout de paramètres supplémentaires
                    'line_id' : current_line.id,
                    'is_accessory' : current_line.is_accessory,
                    'ref' : current_line.ref,
                    'sequence': current_line.sequence,
                    }))

        return {'boms_done' : boms_done, 'lines_done': lines_done}  


# Classe ligne des composants
class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    ref = fields.Char(
        string="Référence")
    is_accessory = fields.Boolean(
        string="Est un accessoire",
        default=False)
    component_exist = fields.Boolean(
        string="Composant existant",
        default=False)
    component_id = fields.Many2one(
        string="identifiant composant",
        comodel_name="mrp.component")

    _sql_constraints = [('reference_unique', 'unique(ref)',
                         'Il y a des doublons dans la colonne référence!')]

    #Fonction manokatr popup any am sous-composant n nomenclature
    @api.multi
    def open_view_component(self):
        product_id = self.product_id
        id = self.id
        view_ref = self.env.ref('mrp_mim.mrp_configuration_component_view')
        component_exist = self.component_exist
#       Si la configuration du composant n'existe pas encore, elle sera créée
        if not component_exist:
            return {
                'name': ('Configuration des composants'),
                'res_model': 'mrp.component',
                'type': 'ir.actions.act_window',
                'view_id': view_ref.id,
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'new',
                'nodestroy': True,
                'context': {
                        'default_product_parent_id': product_id.id,
                        'default_line_id': id,
                        'default_component_exist': component_exist},
            }
#       dans le cas contraire accède à la configuration du composant
#       en récupérant component_id à partir de line_id
        else:
            component_id = self.component_id
            return {
                'name': ('Configuration des composants'),
                'res_model': 'mrp.component',
                'res_id': component_id.id,
                'type': 'ir.actions.act_window',
                'view_id': view_ref.id,
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'new',
                'nodestroy': True,
            }


# Classe des sous-composants
class MrpSubComponent(models.Model):
    _name = 'mrp.sub.component'

    name = fields.Char(
        string="Désignation")
    python_product_qty = fields.Text(
        string="Quantité unitaire (QU)",
        required=True,
        default="result=0.0")
    python_product_qty_total = fields.Text(
        string="Quantité total (QT)",
        required=True,
        default="result=QU*Q")
    python_len_unit = fields.Text(
        string="Longueur unitaire (LU)",
        required=True,
        default="result=0.0")
    python_len_total = fields.Text(
        string="Longueur total (LT)",
        required=True,
        default="result=LU*QT")
    component_id = fields.Many2one(
        string="Sous-composants",
        comodel_name="mrp.component",
        inverse_name="sub_component_ids")


# Classe de configuration d'un composant : gestion des sous-composants
class MrpComponent(models.Model):
    _name = 'mrp.component'

    def _get_product_parent_id(self):
        return self.env.context.get('product_parent_id')

    def _get_line_id(self):
        return self.env.context.get('line_id')

    def _get_component_exist(self):
        return self.env.context.get('component_exist')

    product_parent_id = fields.Many2one(
        string="Article Parent",
        comodel_name="product.product",
        default=_get_product_parent_id)
    line_id = fields.Many2one(
        string="BOM Line parent",
        comodel_name="mrp.bom.line",
        default="_get_line_id")
    variable = fields.Text(
        string="Variable utilisables",
        help="Variables utilisables dans les calculs en code python",
        readonly=True,
        default=u"""
            Q : Quantité article parent
            largeur : Largeur de l'article
            hauteur : Hauteur de l'article
            QU : Quantité unitaire
            QT : Quantité total
            LU : Longueur unitaire
            style : fr ou en
            vitre : standard
                    pleine_bardage
                    pleine_2_3
                    pleine_1_2
                    pleine_1_3 (remplissage vitre)""")
    sub_component_ids = fields.One2many(
        string="Sous-composants",
        comodel_name="mrp.sub.component",
        inverse_name="component_id",
        copy=True)

    @api.model
    def create(self, vals):
        record = super(MrpComponent, self).create(vals)
        record.line_id.component_exist = True
        record.line_id.component_id = record
        return record
