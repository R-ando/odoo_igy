# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MrpBom(models.Model):
    _inherit = 'mrp.bom'


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    @api.multi
    def open_view_component(self):
        product_id = self.product_id
        id = self.id
        view_ref = self.env.ref('mrp_mim.mrp_configuration_component_view')
        if not component_exist:
            return {
                'name': _('Ajout des sous-composants'),
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
                        'default_component_exist': component_exist,
                           },
                    }

    ref = fields.Char(string="Référence")
    is_accessory = fields.Boolean(string="Est un accessoire", default=False)
    component_exist = fields.Boolean(
        string="Composant existant",
        default=False)
    component_id = fields.Integer(string="Composant")

    _sql_constraints = [('reference_unique', 'unique(ref)',
                         'Il y a des doublons dans la colonne référence!')]


class MrpSubComponent(models.Model):
    _name = 'mrp.sub.component'

    name = fields.Char(string="Désignation")
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


class MrpComponent(models.Model):
    _name = 'mrp.component'

    def _get_product_parent_id(self):
        return self.env.context.get('product_parent_id')

    product_parent_id = fields.Many2one(
        string="Article Parent",
        comodel_name="product.product",
        default=_get_product_parent_id)
    line_id = fields.Many2one(
        string="BOM Line parent",
        comodel_name="mrp.bom.line")
    component_exist = fields.Boolean(
        string="Composant existant")
    variable = fields.Text(
        string="Variable utilisables",
        help="Variables utilisables dans les calculs en code python",
        readonly=True,
        default=u'''
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
                        pleine_1_3 (remplissage vitre)''')
    sub_component_ids = fields.One2many(
        string="Sous-composants",
        comodel_name="mrp.sub.component",
        inverse_name="component_id")
