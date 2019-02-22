from odoo import models,fields

class Cnaps(models.Model):
    _name = 'cnaps'
    _description = 'Etat CNAPS'

    employee_id = fields.Many2one(
        'hr.employee',
        string='Employé',
    )
    num_emp = fields.Char(
    	string='Matricule',
    	size=128,
    	)
    name_related = fields.Char(
        string='Nom',
        size=128,
    )
    basic = fields.Float(
        string='Salaire de base',
    )
    cnaps = fields.Float(
        string='CNAPS Travailleur',
    )
    cnapsemp = fields.Float(
        string='CNAPS Employeur',
    )
    brut = fields.Float(
        string='Salaire Brut',
    )
    net = fields.Float(
        string='Salaire Net',
    )
    date_from = fields.Date(
        string='Start Date'
    )
    date_to = fields.Date(
        string='End Date'
    )
    totalcnaps = fields.Float(
        string='TOTAL CNAPS',
    )

    ref_employeur = fields.Char(
        string='Ref Employeur',
    )
    avantage = fields.Float(
        string='Avantage du mois',
    )
    temps_presence = fields.Float(
        string='Temps de présence',
    )