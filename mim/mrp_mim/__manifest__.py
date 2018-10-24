# -*- coding: utf-8 -*-
{
    'name': 'MRP MIM',
    'version': '2.0',
    'description': """Ce module permet de creer un ordre de fabrication avancees en fonction du nombre, de la largeur et de la hauteur d\'un article. Ce module requiert l\'installation des modules suivants :\n
    * mrp
    * mim_module
    * stock
    """,
    'author': 'INGENOSYA',
    'sequence': 1,
    'website': 'http://mim-madagascar.com',
    'depends': ['mrp', 'product'],
    'data': [
        'views/mrp_bom_view.xml',
        'views/mrp_production_view.xml', ],
    'test': [],
    'installable': True,
    'application': True,
    'images': [],
}
