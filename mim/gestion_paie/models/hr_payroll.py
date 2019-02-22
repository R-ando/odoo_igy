from odoo import models,fields,api
from datetime import date

class HrWageAdvance(models.Model):
    _name = 'hr.wage.advance'

    @api.multi
    def _get_current_employee_id(self):
    	employee_ids = self.env['hr.employee'].search([('user_id','=',self.env.uid)])
    	if employee_ids:
    		return employee_ids.id
    	return False

    @api.multi
    def _get_departement_id(self):
    	employee_ids = self.env['hr.employee'].search([('user_id','=',self.env.uid)])
    	if employee_ids:
    		return employee_ids.department_id.id
    	return False

    @api.multi
    def _get_manager_id(self):
    	employee_ids = self.env['hr.employee'].search([('user_id','=',self.env.uid)])
    	if employee_ids:
    		return employee_ids.parent_id.id
    	return False

    name = fields.Char(
    	string='Nom de la demande',
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string='Demandeur',
        required=True,
        default=_get_current_employee_id,
    )
    department_id = fields.Many2one(
        'hr.department',
        string='Département',
        required=True,
        default=_get_departement_id
    )
    date = fields.Date(
        string='Date de la demande',
        required=True,
        default=date.today().strftime('%Y-%m-%d'),
    )
    amount = fields.Float(
        string='Montant',
    )
    manager_id = fields.Many2one(
        'hr.employee',
        string='Responsable',
        required=True,
        default=_get_manager_id,
    )
    state = fields.Selection(
    	[
	    	('draft','Nouveau'),
	    	('ok','Validé'),
	    	('not_ok','Refusé'),
    	],
    	string='Etat',
    	default='draft',
    	track_visibility='onchange',
    )

    @api.onchange('employee_id')
    def onchange_employee_id(self):
    	self.name = 'Demande de' + self.employee_id.name
    	# return 

    @api.multi
    def accept_avance(self):
    	self.write({
    		'state' : 'ok',
    		})
    	return True

    @api.multi
    def deny_avance(self):
    	self.write({
    		'state' : 'not_ok',
    		})
    	return True

class HrPayrollInterim(models.Model):
    _name = 'hr.payroll.interim'

    @api.multi
    def _get_current_employee_id(self):
    	employee_ids = self.env['hr.employee'].search([('user_id','=',self.env.uid)])
    	if employee_ids:
    		return employee_ids.id
    	return False

    @api.multi
    def _get_departement_id(self):
    	employee_ids = self.env['hr.employee'].search([('user_id','=',self.env.uid)])
    	if employee_ids:
    		return employee_ids.department_id.id
    	return False

    @api.multi
    def _get_manager_id(self):
    	employee_ids = self.env['hr.employee'].search([('user_id','=',self.env.uid)])
    	if employee_ids:
    		return employee_ids.parent_id.id
    	return False

    employee_id = fields.Many2one(
        'hr.employee',
        string='Demandeur',
        required=True,
        default=_get_current_employee_id,
    )
    department_id = fields.Many2one(
        'hr.department',
        string='Département',
        required=True,
        default=_get_departement_id
    )
    manager_id = fields.Many2one(
        'hr.employee',
        string='Responsable',
        required=True,
        default=_get_manager_id,
    )