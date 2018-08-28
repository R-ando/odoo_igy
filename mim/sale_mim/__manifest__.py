# -*- coding: utf-8 -*-
{
    'name': 'Sale MIM',
    'version': '2.0',
    'sequence': 1,
    'category': 'Sale',
    'description': """This module allows to add sales order lines with specific fields""",
    'author': 'Ingenosya Madagascar',
    'website': 'http://www.ingenosya.mg',
    'depends': ['sale'],
    'data': [
        'views/sale_view.xml',
        'wizard/sale_order_line_advance_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}