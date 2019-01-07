# -*- coding: utf-8 -*-

<<<<<<< HEAD
from odoo import models, fields
=======
from odoo import models, fields, api
>>>>>>> 5bec217211feeae309b49c6f249c9e8946e85c8a


class MrpProductionProductLine(models.Model):

    _name = 'mrp.production.product.line'

    is_accessory = fields.Boolean(
        string="Est un accessoire")
    line_id = fields.Many2one(
        string="Bom Line parent",
        comodel_name="mrp.bom.line")

<<<<<<< HEAD
    def product_id_change(self, product_id):
        if product_id:
            product = self.env['product.product'].product_id
=======
    @api.multi
    def product_id_change(self, product_id):
        if product_id:
            # retourne un objet; browse(product_id).id ny taloha
            product = self.env['product.product'].browse(product_id)
>>>>>>> 5bec217211feeae309b49c6f249c9e8946e85c8a
            product_id_vals = {
                'product_uom': product.uom_id.id,
                'name': product.name
            }
        return {'value': product_id_vals}


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
<<<<<<< HEAD
        comodel_name="mrp.production")
=======
        comodel_name="mrp.production",
        ondelete='cascade',
        )
>>>>>>> 5bec217211feeae309b49c6f249c9e8946e85c8a


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
<<<<<<< HEAD
        comodel_name="mrp.production")
=======
        comodel_name="mrp.production",
        ondelete='cascade',
        )
>>>>>>> 5bec217211feeae309b49c6f249c9e8946e85c8a
