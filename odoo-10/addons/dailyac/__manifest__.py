# -*- coding: utf-8 -*-
{
    'name': "dailyac",

    'summary': """
        Registro de Actividades Diarias
        """,

    'description': """
        Modulo que permite tener un registro detallado de todas
        las actividades diarias que realiza una persona en su
        dia a dia.
    """,

    'author': "Victor Pino",
    'website': "http://www.p2++.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/activity.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}