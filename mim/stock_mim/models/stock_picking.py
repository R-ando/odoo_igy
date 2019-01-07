# -*- coding: utf-8 -*-

from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

# bon de livraison 1
    motivation = fields.Text(
        string="Motivation")
    date_changed = fields.Boolean(
        string=u"Date changée",
        default=False)

# stock_mim_final/stock_move_split
    state = fields.Selection(
        string="Status",
        selection=[
            ('draft', 'Draft'),
            ('waiting', 'Waiting Another Operation'),
            ('confirmed', 'Waiting'),
            ('contre_mesure', 'Contre mesure'),
            ('flowsheeting', u'Fiche de Débit'),
            ('assigned', 'Ready'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
        ],
        compute='_compute_state',
        copy=False, index=True, readonly=True, store=True,
        track_visibility='onchange',
        help=" * Draft: not confirmed yet and will not be scheduled until confirmed.\n"
             " * Waiting Another Operation: waiting for another move to proceed before it becomes automatically available (e.g. in Make-To-Order flows).\n"
             " * Waiting: if it is not ready to be sent because the required products could not be reserved.\n"
             " * Ready: products are reserved and ready to be sent. If the shipping policy is 'As soon as possible' this happens as soon as anything is reserved.\n"
             " * Done: has been processed, can't be modified or cancelled anymore.\n"
             " * Cancelled: has been cancelled, can't be confirmed anymore."

    )

# stock_mrp
    mo_created = fields.Boolean(
        string="Ordre de fabrication créé")
    late_production = fields.Float(
        string="Retard de production (Jours)")
    production_date = fields.Datetime(
        string="Date de fin de production")
    late_delivery = fields.Float(
        string="Retard de livraison (Jours)")
    delivery_date = fields.Datetime(
        string="Date de fin de livraison")
    is_old_picking_assigned = fields.Boolean(
        string="Ancien BL disponible",
        default=False)
    is_old_picking_done = fields.Boolean(
        string="Ancien BL terminé",
        default=False)
    mo_created_copy = fields.Boolean(
        string="Ordre de fabrication créé ?")

# stock_state
    confirmed = fields.Char(
        string=u"Attente de disponibilité")
    contre_mesure = fields.Char(
        string="Contre Mesure")
    fiche_debit = fields.Char(
        string=u"Fiche de débit")
    assigned = fields.Char(
        string="Disponible")
    done = fields.Char(
        string=u"Terminé")
    total = fields.Char(
        string="Total")
