# -*- coding: utf-8 -*-

from odoo import models, fields

#classe pour stocker les lignes du produits
class MrpProductionProductLine(models.Model):

    _name = 'mrp.production.product.line'

    is_accessory = fields.Boolean(
        string="Est un accessoire")
    line_id = fields.Many2one(
        string="Bom Line parent",
        comodel_name="mrp.bom.line")
    production_id = fields.Many2one(
        comodel_name='mrp.production',
        string='Production Order',
    )
    product_qty = fields.Float(
        string='Product Qty',
    )
    name = fields.Text(
        string='Name',
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
    )
    product_uom_id = fields.Many2one(
        'product.uom',
        string='Uom Product',
    )

    def product_id_change(self, product_id):
        if product_id:
            product = self.env['product.product'].product_id
            product_id_vals = {
                'product_uom': product.uom_id.id,
                'name': product.name
            }
        return {'value': product_id_vals}


#Classe pour stocker les composants de la nomenclature
class MrpProductionProductComponentLine(models.Model):
    _name = 'mrp.production.product.component.line'

    ref = fields.Char(
        string="Référence")
    name = fields.Char(
        string="Description")
    product_qty = fields.Float(
        string="Quantité unitaire")
    product_qty_total = fields.Float(
        string="Quantité total")
    len_unit = fields.Float(
        string="Longueur unitaire")
    len_total = fields.Float(
        string="Longueur total")
    production_id = fields.Many2one(
        string="Production Order",
        comodel_name="mrp.production")

#Classe pour stocker les accessoires de la nomenclature
class MrpProductionProductAccessoryLine(models.Model):
    _name = 'mrp.production.product.accessory.line'

    ref = fields.Char(
        string="Référence")
    name = fields.Char(
        string="Description")
    product_qty = fields.Float(
        string="Quantité unitaire")
    product_qty_total = fields.Float(
        string="Quantité total")
    production_id = fields.Many2one(
        string="Production Order",
        comodel_name="mrp.production")
