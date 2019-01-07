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
<<<<<<< HEAD
    'depends': ['mrp', 'product', 'sale_mim','stock_account'],#CPR+stock_account
=======
    'depends': ['mrp', 'product', 'sale_mim'],
>>>>>>> 5bec217211feeae309b49c6f249c9e8946e85c8a

    # always loaded
    'data': [
        'views/mrp_bom_view.xml',
        'views/mrp_production_view.xml',
<<<<<<< HEAD
        'wizard/mrp_production.xml',
        # 'views/mrp_production_product_view.xml',
=======
        # 'views/mrp_production_product_view.xml',
        'views/mrp_view.xml',
>>>>>>> 5bec217211feeae309b49c6f249c9e8946e85c8a
    ],

    'icon': 'mrp_mim/static/src/img/icon.png',
    'application': True,
    'installable': True,
    'auto_install': False,
}
