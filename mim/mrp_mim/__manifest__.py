# -*- coding: utf-8 -*-
{
    'name': "Gestion de Fabrication MIM",

    'summary': """ """,

    'description': u"""
        Gestion des fabrications de MIM:
            - Articles composés par des sous-composants
            - Ordre de fabrication avancé : largeur, hauteur
    """,

    'author': "Ingenosya Madagascar",
    'website': "http://www.ingenosya.mg",
    'category': 'Mrp',
    'version': '3.0',
    'sequence': 1,
    # any module necessary for this one to work correctly
    'depends': ['mrp', 'product', 'sale_mim'],

    # always loaded
    'data': [
        'views/mrp_bom_view.xml',
        'views/mrp_production_view.xml',
        'views/mrp_raw_materials_count_view.xml',
        'views/mrp_view.xml',
    ],

    'icon': 'mrp_mim/static/src/img/icon.png',
    'application': True,
    'installable': True,
    'auto_install': False,
}
