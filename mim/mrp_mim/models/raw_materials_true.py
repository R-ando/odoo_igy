import logging

from odoo import models
from odoo import fields
from odoo import api
from odoo import exceptions


class RawMaterialsCount(models.Model):
    """ Count raw materials from mrp.production when
    the method action_compute is called"""

    _name = 'mrp.rawmaterials.count'

    product_name = fields.Char(
        string='Artciles'
    )

    product_id = fields.Integer(
        string='Id produit'
    )

    product_qty = fields.Float(
        string=u'Quantités',
        default=0.0
    )

    product_uom_name = fields.Char(
        string=u'Unités de mesures'
    )

    product_uom_id = fields.Integer(
        string=u'Id Unité de mesure'
    )

    product_cat_name = fields.Char(
        string=u'Catégories'
    )
