# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.addons.agili.common.utils import FORMA_DATE, validKey, workDays, sendEmail, daysExe
from datetime import datetime, date

class Project(models.Model):

    _name = 'agili.project'

    name = fields.Char(string="Nombre del Proyecto", 
                       required=True,
                       unique=True)

    description = fields.Text(string="Descripción")

    start_date = fields.Date(string="Fecha de inicio")

    end_date = fields.Date(string="Fecha de Fin")

    days_plan = fields.Integer(string="Dias planificados", 
                                    compute='_diasLaborales')

    days_exe = fields.Integer(string="Dias ejecutados")

    pj_progress = fields.Float(string="Porcentaje de Avance")

    pj_work_real = fields.Integer(string="Reporte de avance real en dias")

    responsible_ids = fields.Many2many('res.users', 
                                        string="Responsables",
                                        required=True)

    milestone_ids = fields.One2many('agili.milestone', 
                        'ms_project_id', 
                        string="Hitos")


    _sql_constraints = [
        ('name_description_check',
        'CHECK(name != description)',
        "El nombre del proyecto no puede ser la descripción."),

        ('name_unique',
        'UNIQUE(name)',
        "El nombre del proyecto es unico"),

        ('days_valid',
        'CHECK(days_plan > 0)',
        "Los dias planificados tienen que ser mayor a 0"),
    ]

    @api.depends('start_date', 'end_date')
    def _diasLaborales(self):
        
        for r in self:

            if r.start_date != False and r.end_date != False:

                r.days_plan = workDays(r.start_date, r.end_date)

    @api.depends('start_date')
    def _daysexe(self):

        for r in self:

            if r.start_date != False and r.end_date != False:

                r.days_exe = daysExe(r.start_date, r.end_date)


    @api.multi
    def send_alert(self):

        print "Entro en la funcion de enviar correos"

        projects = self.env['agili.project'].search([('days_plan','>=', 0)])

        for project in projects:

            print "Entro en el for de los proyectos"

            ini_date = project.start_date
            end_date = project.end_date

            ini_date = datetime.strptime(ini_date, FORMA_DATE)
            end_date = datetime.strptime(end_date, FORMA_DATE)
            today = datetime.now()

            today_diff = str((end_date-today).days)
            days_diff = str((end_date-ini_date).days) 

            if days_diff >= 3 and project.pj_progress <= 70 and today_diff <=3 or today_diff == 0 and project.pj_progress < 100:

                print "El proyecto cumple con las condiciones para enviarle un correo"
                
                responsibles = []

                for responsible in project.responsible_ids:

                    responsibles.append(responsible.email)

                info = {}

                info['name'] = project.name
                info['end_date'] = end_date
                info['days_plan'] = days_plan
                info['days_exe'] = days_exe

                addressee = responsibles
                
                response = sendEmail(addressee, info, emitter=None)

    @api.model
    def print_report(self):

        context = self.env.context
    
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'agili.report_project_general',
            'context': context,
        }
