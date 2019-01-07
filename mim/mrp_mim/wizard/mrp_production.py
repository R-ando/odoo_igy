from odoo import models, fields, api, exceptions

class MrpProduction(models.TransientModel):
    _inherit = "stock.quantity.history"

    article = fields.Char(string="name")
    quantite = fields.Integer(string="product_qty")
    unite_de_mes = fields.Integer(string="product_uom_id")

    # def compute_quantity(self, date):
    #     request_1 = "select product_qty from mrp_bom_line where write_date >= %s and write_date < (select max(write_date) from mrp_bom_line)', (date,)"

