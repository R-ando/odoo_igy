
{
	'name' : 'Paie Malagasy',
	'category' : 'Human Ressources',
	'version' : '3.0',
	'sequence' : 1,
	'description' : 'Gestion de paie Malagasy',
	'website' : 'https://www.ingenosya.com',
	'depends' : ['hr_contract','hr_payroll','base'],
	'data' : [
				'views/paie_view.xml',
				'views/etat_salaire_view.xml',
				'views/cnaps_view.xml',
				'views/ostie_view.xml',
				'views/irsa_view.xml',
				'views/hr_payroll_view.xml',
                'report/report_fiche_de_paie.xml',
				# 'data/hr_payroll_data.xml',
			],

	'icon' : 'paie_mim/static/src/img/icon.png',
	'installable' : True,
	'application' : True,
	'auto_install' : False,
}
