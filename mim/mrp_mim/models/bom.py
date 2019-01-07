# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


# Classe nomenclature des articles
class MrpBom(models.Model):
    _inherit = 'mrp.bom'


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
    # compoenent_id =>fiels.integer dans source
    component_id = fields.Many2one(
        string="identifiant composant",
        comodel_name="mrp.component")

    _sql_constraints = [('reference_unique', 'unique(ref)',
                         'Il y a des doublons dans la colonne référence!')]

    @api.multi
    def open_view_component(self):
        product_id = self.product_id
        id = self.id
        view_ref = self.env.ref('mrp_mim.mrp_configuration_component_view')
        component_exist = self.component_exist
#       Si la configuration du composant n'existe pas encore, elle sera créée
        if not component_exist:
            return {
                'name': _('Configuration des composants'),
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
                'name': _('Configuration des composants'),
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
        comodel_name="mrp.component")


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


# class MrpProductionProductLine(models.Model):
#     _inherit = 'mrp.production.product.line'
 
#     is_accessory = fields.Boolean(
#         string=u'Est un accesoire',
#     )
    
#     line_id = fields.Many2many(
#         string=u'line_id',
#         comodel_name='mrp.bom.line',
#         ondelete='cascade',    
#     )
