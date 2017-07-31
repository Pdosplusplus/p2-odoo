# -*- coding: utf-8 -*-
{
    'name': "SIGESALUD",

    'summary': """
        Gestión de la póliza del seguro colectivo
        """,

    'description': """
        El proyecto de gestión de la póliza del seguro colectivo surge por la necesidad de
        gestionar un sistema que automatice los procesos de administración del beneficio
        de salud colectivo y la generación de estadísticas que comprueben el uso de la
        póliza de seguro contratada por parte del colectivo beneficiado.
        
        Las cooperativas que se unen como colectivo para usar la póliza HCM son: la
        Asociación Cooperativa Geekos R.L, la Asociación Cooperativa Vultur R.L, la
        Asociación Cooperativa Bmkeros R.L, la Asociación Cooperativa Tecnoparaguana
        R.L y la Asociación Cooperativa SinapSys R.L.

        Se requiere un sistema que gestione los expedientes de los beneficiarios, mantenga
        un soporte digital de los documentos que acompañan cada transacción y genere los
        reportes y estadísticas requeridas por el colectivo para hacer seguimiento y control
        de los procesos asociados al uso de la póliza.
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
        'security/sigesalud_security.xml',
        'security/ir.model.access.csv',
        'views/expedient_view.xml',
        'views/disease_view.xml',
        'views/beneficiary_view.xml',
        'views/support_view.xml',
        'views/event_view.xml',
        'views/exam_view.xml',
        'views/policy_view.xml',
        'views/res_users_view.xml',
        'reports/report_expedient.xml',
        'reports/report_mounthly.xml',
        'reports/sigesalud_report.xml',
        'reports/report_repayment.xml',
        'views/repayment_view.xml',
        'views/cron_view.xml',
        'wizard/sigesalud_report_monthly_view.xml',
    ],
    
    'qweb': [
        
    ],
    
    'js': [
        
    ],

    'application': True,
    'installable': True,

}