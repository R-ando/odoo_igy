# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def _get_user_id(self):
        return self._context.get('user_id')

#   Make_invoice
    user_id = fields.Many2one(
        string="Salesperson",
        comodel_name="res.users",
        readonly=True,
        default='_get_user_id')
