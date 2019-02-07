# -*- coding: utf-8 -*-
{
    'name': "Gestion de Vente MIM",

    'summary': """ """,

    'description': u"""
        Gestion des ventes de MIM:
            - Ajouter des lignes de commandes spécifiques
            - Articles et produits MIM
    """,

    'author': "Ingenosya Madagascar",
    'website': "http://www.ingenosya.mg",
    'category': 'Sale',
    'version': '3.0',
    'sequence': 1,
    # any module necessary for this one to work correctly
    'depends': ['sale', 'product'],

    # always loaded
    'data': [
        'views/sale_view.xml',
        'views/product_view.xml',
        'views/sale_count_bom.xml',
        'views/sale_count_all_bom.xml',
        'wizard/sale_order_line_advance_view.xml',
        'wizard/sale_order_line_count_wizard.xml',
    ],

    'icon': 'sale_mim/static/src/img/icon.png',
    'application': True,
    'installable': True,
    'auto_install': False,
}
