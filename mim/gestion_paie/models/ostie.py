from odoo import models,fields

class Ostie(models.Model):
    _name = 'ostie'
    _description = 'Etat ostie'

    employee_id = fields.Many2one(
        'hr.employee',
        string='Employé',
    )
    num_emp = fields.Char(
        string='Matricule',
        size=128,
    )
    num_cin = fields.Char(
        string='CIN',
        size=128,  
    )
    name_related = fields.Char(
        string='Nom',
        size=128,  
    )
    basic = fields.Float(
        string='Salaire de base', 
    )
    omsi = fields.Float(
        string='OMSI Travailleur', 
    )
    omsiemp = fields.Float(
        string='OMSI Employeur', 
    )
    brut = fields.Float(
        string='Salaire Brut', 
    )
    net = fields.Float(
        string='Salaire Net', 
    )
    date_from = fields.Date(
        string='Start Date', 
    )
    date_to = fields.Date(
        string='End Date', 
    )
    totalomsi = fields.Float(
        string='TOTAL OMSI', 
    )

    avantage = fields.Float(
        string='Avantage du mois', 
    )
    temps_presence = fields.Float(
        string='Temps de présence',
    )