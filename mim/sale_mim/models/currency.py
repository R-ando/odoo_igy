# -*- coding: utf-8 -*-

from odoo import models, fields


class Currency(models.Model):
    _inherit = 'res.currency'

#   Add_image
    currency_name = fields.Char(
        string="Nom complet devise",
        size=20)
<<<<<<< HEAD


=======
>>>>>>> 5bec217211feeae309b49c6f249c9e8946e85c8a
