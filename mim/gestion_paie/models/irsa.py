from odoo import models,fields

class Ostie(models.Model):
    _name = 'irsa'
    _description = 'Etat irsa'

    employee_id = fields.Many2one(
        'hr.employee',
        string='Employé',
        readonly=False,
    )
    num_emp = fields.Char(
        string='Matricule',
        size=128,
        readonly=False,
    )
    num_cin = fields.Char(
        string='CIN',
        size=128,
        readonly=False,  
    )
    name_related = fields.Char(
        string='Nom',
        size=128,
        readonly=False,  
    )
    basic = fields.Float(
        string='Salaire de base',
        readonly=False, 
    )
    brut = fields.Float(
        string='Salaire Brut',
        readonly=False, 
    )
    net = fields.Float(
        string='Salaire Net',
        readonly=False, 
    )
    irsa = fields.Float(
        string='IRSA',
        readonly=False, 
    )
    date_from = fields.Date(
        string='Start Date',
        readonly=False, 
    )
    date_to = fields.Date(
        string='End Date',
        readonly=False, 
    )
    avantage = fields.Float(
        string='Avantage du mois',
        readonly=False, 
    )