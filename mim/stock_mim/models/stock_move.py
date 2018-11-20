# -*- coding: utf-8 -*-

from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    user_id = fields.Many2one(
        string="Créateur de l'Ordre de Fabrication",
        comodel_name="res.users")
# mrp
    id_mo = fields.Integer(
        string="Id manufacturing order")
    is_mo_created = fields.Boolean(
        string="Ordre de fabrication créé",
        default=False)
    is_printable = fields.Boolean(
        string="Fiche de débit standard",
        default=False)
    in_mrp_valider_group = fields.Boolean(
        string='Utilisateur courant dans le groupe "Valider fiche de débit"')

    largeur = fields.Float(
        string="Largeur")
    hauteur = fields.Float(
        string="Hauteur")

# stock_mim_final
    state = fields.Selection(
        string="Status",
        selection=[
            ('draft', 'New'), ('cancel', 'Cancelled'),
            ('waiting', 'Waiting Another Move'),
            ('confirmed', 'Waiting Availability'),
            ('partially_available', 'Partially Available'),
            ('assigned', 'Available'),
            ('done', 'Done')
        ],
        copy=False, default='draft', index=True, readonly=True,
        help="* New: When the stock move is created and not yet confirmed.\n"
             "* Waiting Another Move: This state can be seen when a move is waiting for another one, for example in a chained flow.\n"
             "* Waiting Availability: This state is reached when the procurement resolution is not straight forward. It may need the scheduler to run, a component to be manufactured...\n"
             "* Available: When products are reserved, it is set to \'Available\'.\n"
             "* Done: When the shipment is processed, the state is \'Done\'."
    )

    state = fields.Selection([
        ('draft', 'New'), ('cancel', 'Cancelled'),
        ('waiting', 'Waiting Another Move'),
        ('confirmed', 'Waiting Availability'),
        ('partially_available', 'Partially Available'),
        ('assigned', 'Available'),
        ('done', 'Done')], string='Status',
        copy=False, default='draft', index=True, readonly=True,
        help="* New: When the stock move is created and not yet confirmed.\n"
             "* Waiting Another Move: This state can be seen when a move is waiting for another one, for example in a chained flow.\n"
             "* Waiting Availability: This state is reached when the procurement resolution is not straight forward. It may need the scheduler to run, a component to be manufactured...\n"
             "* Available: When products are reserved, it is set to \'Available\'.\n"
             "* Done: When the shipment is processed, the state is \'Done\'.")

# stock_mrp
    name = fields.Text(
        string="Description")
