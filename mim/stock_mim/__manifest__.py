# -*- coding: utf-8 -*-
{
    'name': "Gestion de Stock MIM",

    'summary': """ """,

    'description': u"""
        Gestion des stocks de MIM:
            - Mouvements de stock
            - Bilan de stocks
            - Stock et matériels de fabrication
    """,

    'author': "Ingenosya Madagascar",
    'website': "http://www.ingenosya.mg",
    'category': 'Mrp',
    'version': '3.0',
    'sequence': 1,
    # any module necessary for this one to work correctly
    'depends': ['stock', 'product', 'mrp'],

    # always loaded
    'data': [
        'views/stock_picking.xml',
        'views/stock_move.xml',
    ],

    'icon': 'mrp_mim/static/src/img/icon.png',
    'application': True,
    'installable': True,
    'auto_install': False,
}
