
from odoo import models
from odoo import api
from odoo import fields


class RawMaterials(models.Model):
    _inherit = 'product.template'

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
