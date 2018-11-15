# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

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


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

#   Add_image
    image = fields.Binary('Image')
