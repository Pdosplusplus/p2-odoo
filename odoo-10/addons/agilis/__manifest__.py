# -*- coding: utf-8 -*-
{
    'name': "agilis",

    'summary': """
        Gestion y Control de las Cooperetivas
        """,

    'description': """
        Modulo que permite la gestion de todos los proyectos
        que son llevados y ejecutados por la red de cooperativas
    """,

    'author': "Geekos",
    'website': "http://geekos.co.ve/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'report',
        'auditlog',
    ],

    # always loaded
    'data': [
        'security/agilis_security.xml',
        'security/ir.model.access.csv',
        'views/res_users_view.xml',
        'views/project_view.xml',
        'views/cooperative_view.xml',
        'views/trimestre_view.xml',
        'views/service_view.xml',
        'views/measure_view.xml',
        'views/load_view.xml',
        'views/activity_view.xml',
        'views/advance_view.xml',
        'views/bitacora_view.xml',
    ],
    
    'qweb': [
        'static/src/xml/custom_button_header_tree_qweb.xml',
    ],
    
    'js': [
        'static/src/js/action_button_header_tree.js',
    ],

    'application': True,
    'installable': True,

}