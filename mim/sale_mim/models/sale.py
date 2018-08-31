# -*- coding: utf-8 -*-

from odoo import fields, api, models


class sale_order(models.Model):
    _inherit = 'sale.order'
    
    entete = fields.Text('Sujet')
    note = fields.Text('Terms and conditions')
    
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
            'name': 'Configuration article',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order.line.advance',
            'target': 'new',
            'context': ctx,
            }
 

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
#     @api.depends('largeur', 'hauteur')
#     def _get_dimension(self):
#         for line in self:
#             line.dim = self.width + ' x ' + self.height
         
    #dim = fields.Char('Dimension', compute='_get_dimension', readonly=True)
    
    image = fields.Binary('Image')
