# -*- coding: utf-8 -*-
{
    'name': "agili",

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
        'security/agili_security.xml',
        'security/ir.model.access.csv',
        'views/project.xml',
        'views/activity.xml',
        'views/deliverable.xml',
        'views/report_general_js.xml',
        'views/webclient_templates.xml',
        'wizard/agili_report_project_specific_view.xml',
        'reports/report_project_general.xml',
        'reports/report_project_specific.xml',
        'reports/report_project_view.xml',
        'reports/agili_report.xml',
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