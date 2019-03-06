from odoo import models,fields

class EtatSalaire(models.Model):
    _name = 'etat.salaire'
    _description = 'Etat global des salaires'

    employee_id = fields.Many2one(
        'hr.employee',
        string='Employé',
        readonly=True,
    )
    num_emp = fields.Char(
        string='Matricule',
        size=128,
        readonly=True,
    )
    num_cin = fields.Char(
        string='CIN',
        size=128,
        readonly=True,  
    )
    name_related = fields.Char(
        string='Nom',
        size=128,
        readonly=True,  
    )
    basic = fields.Float(
        string='Salaire de base',
        readonly=True, 
    )
    omsi = fields.Float(
        string='OMSI Travailleur',
        readonly=True, 
    )
    omsiemp = fields.Float(
        string='OMSI Employeur',
        readonly=True, 
    )
    cnaps = fields.Float(
        string='CNAPS Travailleur',
        readonly=True, 
    )
    cnapsemp = fields.Float(
        string='CNAPS Employeur',
    )
    brut = fields.Float(
        string='Salaire Brut',
        readonly=True, 
    )
    net = fields.Float(
        string='Salaire Net',
        readonly=True, 
    )
    irsa = fields.Float(
        string='IRSA',
        readonly=True, 
    )
    date_from = fields.Date(
        string='Start Date',
        readonly=True, 
    )
    date_to = fields.Date(
        string='End Date',
        readonly=True, 
    )
    totalcnaps = fields.Float(
        string='TOTAL CNAPS',
        readonly=True, 
    )
    totalomsi = fields.Float(
        string='TOTAL OMSI',
        readonly=True, 
    )