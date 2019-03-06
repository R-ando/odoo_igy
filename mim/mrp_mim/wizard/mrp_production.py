# -*- coding: utf-8 -*-
from odoo import models, fields, api


class RawMaterials(models.TransientModel):
    _name = 'stock.wizard'
    _inherit = 'product.template'

    x = fields.Many2one('stock.temp')
    is_bom = fields.Boolean(
        string='is_bom',
        compute='_bom_line',
        store=True
    )

    @api.multi
    def _bom_line(self):
        bom_line = self.env['mrp.bom.line']
        for record in self:
            search_id = bom_line.search([('product_id', '=', record.id)])
            if search_id:
                record.is_bom = True
            else:
                record.is_bom = False




class Temp(models.TransientModel):
    _name = 'stock.temp'

    t = fields.One2many('stock.wizard','x', compute="open_rec")

    @api.multi
    def open_rec(self):
        return {
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'stock.temp',
                'res_id': self.id,
                'type': 'ir.actions.act_window',
                'target': 'new',
                'flags': {'form': {'action_buttons': True}}
        }




# class MrpProduction(models.TransientModel):
#     _name = "stock.wizard"

#     article = fields.Char(string="Article")
#     quantity  = fields.Integer(string="Quantité")
#     uom = fields.Char(string="Unité")
#     x = fields.Many2one('stock.temp')



# class Temp(models.TransientModel):
#     _name = "stock.temp"

#     t = fields.One2many('stock.wizard','x')









