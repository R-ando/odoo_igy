# -*- coding: utf-8 -*-
{
    'name': u'Mise à jour des champs calculés',

    'summary': u""" """,

    'description': """
        Actualisation des champs calculés:
            - Mise à jour des champs calculés
    """,

    'author': "Ingenosya Madagascar",
    'website': "http://www.ingenosya.mg",
    'category': 'Base',
    'version': '3.0',
    'sequence': 1,
    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/view_migration.xml',
    ],

    'icon': 'refresh_fields/static/src/img/icon.png',
    'application': True,
    'installable': True,
    'auto_install': False,
}
