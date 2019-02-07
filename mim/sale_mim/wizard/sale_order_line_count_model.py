from odoo import _
from odoo import models

class SaleOrderLineCount(models.TransientModel):
    _name = 'sale.order.line.count'
    _description = 'Transcient model to avoid using qweb, lol :D'

    def open_table(self):
        # load sale.count.bom
        sale_order_line_objs = self.env['sale.order']
        sale_order_line_objs.action_count_all()

        return {
            'name': _('Consommation bom'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.count.bom',
            'target': 'current',
        }
