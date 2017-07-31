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


    journeys_plan = fields.Integer(string="Jornadas Planificadas")

    journeys_exe = fields.Integer(string="Jornadas Ejecutadas")

    pj_amount = fields.Float(string="Monto del proyecto")

    pj_progress = fields.Float(string="Porcentaje de Avance")

    responsible_ids = fields.Many2many('res.users', 
                                        string="Responsables",
                                        required=True)

    milestone_ids = fields.One2many('agili.milestone', 
                        'ms_project_id', 
                        string="Hitos")

    deliverable_ids = fields.One2many('agili.deliverable', 
                        'dl_project_id', 
                        string="Entregables")

    activity_ids = fields.One2many('agili.activity', 
                        'ac_project_id', 
                        string="Entregables")


    _sql_constraints = [
        ('name_description_check',
        'CHECK(name != description)',
        "El nombre del proyecto no puede ser la descripción."),

        ('name_unique',
        'UNIQUE(name)',
        "El nombre del proyecto es unico"),
    ]

    @api.multi
    def send_alert(self):

        projects = self.env['agili.project'].search([('id','>=', 0)])

        for project in projects:

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

