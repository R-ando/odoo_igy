# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductProduct(models.Model):

    _inherit = 'product.product'

    ref = fields.Char(
        string=u"Référence")
