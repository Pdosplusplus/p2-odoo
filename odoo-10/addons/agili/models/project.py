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
                                    compute='_diasLaborales',
                                    store=True)

    days_exe = fields.Integer(string="Dias ejecutados",
                              compute="_daysexe")

    pj_progress = fields.Float(string="Porcentaje de Avance",
                              compute="_progress")

    pj_work_real = fields.Integer(string="Reporte de avance real",
                                 compute="_workplan")

    responsible_ids = fields.Many2many('res.users', 
                                        string="Responsables",
                                        required=True)

    workplan_id = fields.Many2one('agili.workplan',
                                ondelete='cascade', 
                                string="Plan de trabajo")

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

            if r.start_date and r.end_date:

                r.days_plan = workDays(r.start_date, r.end_date)

    @api.depends('start_date')
    def _daysexe(self):

        for r in self:

            if r.start_date:

                r.days_exe = daysExe(r.start_date)

    @api.depends('workplan_id')
    def _progress(self):
        
        for r in self:
                
            if r.workplan_id:

                r.pj_progress = r.workplan_id.wk_progress

    @api.depends('workplan_id')
    def _workplan(self):
        
        for r in self:
                
            if r.workplan_id:

                r.pj_work_real = r.workplan_id.wk_work_real

    @api.multi
    def send_alert(self):

        projects = self.env['agili.project'].search([('days_plan','>=', 0)])

        for project in projects:

            ini_date = start_date
            end_date = end_date

            ini_date = datetime.strptime(ini_date, FORMA_DATE)
            end_date = datetime.strptime(end_date, FORMA_DATE)
            today = datetime.now()

            today_diff = str((end_date-today).days)
            days_diff = str((end_date-ini_date).days) 

            if days_diff >= 3 and project.pj_progress <= 70 and today_diff <=3:

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


class report_project_general(models.AbstractModel):
    _name = 'report.agili.report_project_general'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('agili.report_project_general')
        projects = self.env['agili.project'].search([('days_plan','>=', 0)])
        
        docargs = {
            'doc_model': report.model,
            'data': self._get_data_general(),
        }

        return report_obj.render('agili.report_project_general', docargs)
        
    def _get_data_general(self):

        data = {}

        data['pro_done'] = 0
        data['pro_process'] = 0
        data['pro_stopped'] = 0

        data['days_done'] = 0
        data['days_process'] = 0 
        data['days_stopped'] = 0

        data['pro_porcen'] = 0
        data['days_total'] = 0
        data['days_porcen'] = 0

        projects = self.env['agili.project'].search([('days_plan','>=', 0)])

        data['len_project'] = len(projects)

        projects_done = []
        projects_stopped = []
        projects_process = []

        for project in projects:

            if project.state == 'done':

                p = {}
                responsibles = []

                p['name'] = project.name

                for respon in project.responsible_ids:

                    r = {}
                    r['name'] = respon.name
                    r['days_plan'] = 0
                    r['days_exe'] = 0

                    for activity in project.activity_ids:

                        if respon.name == activity.ac_responsible_id.name:
                        
                            r['days_plan'] = validKey(activity, "ac_days_plan")

                            r['days_exe'] += validKey(activity, "ac_days_exe")


                    responsibles.append(r)

                p['responsibles'] = responsibles

                projects_done.append(p)

                data['pro_done'] += 1
                data['days_done'] += project.days_plan

            if project.state == 'process':

                p = {}
                responsibles = []

                p['name'] = project.name


                for respon in project.responsible_ids:

                    r = {}
                    r['name'] = respon.name
                    r['days_plan'] = 0
                    r['days_exe'] = 0

                    for activity in project.activity_ids:

                        if respon.name == activity.ac_responsible_id.name:
                        
                            r['days_plan'] = validKey(activity, "ac_days_plan")

                            r['days_exe'] += validKey(activity, "ac_days_exe")


                    responsibles.append(r)

                p['responsibles'] = responsibles


                projects_process.append(p)

                data['pro_process'] += 1
                data['days_process'] +=  project.days_plan


            if project.state == 'stopped':

                p = {}
                responsibles = []

                p['name'] = project.name

                for respon in project.responsible_ids:

                    r = {}
                    r['name'] = respon.name
                    r['days_plan'] = 0
                    r['days_exe'] = 0

                    for activity in project.activity_ids:

                        if respon.name == activity.ac_responsible_id.name:
                        
                            r['days_plan'] = validKey(activity, "ac_days_plan")

                            r['days_exe'] += validKey(activity, "ac_days_exe")


                    responsibles.append(r)

                p['responsibles'] = responsibles

                projects_stopped.append(p)

                data['pro_stopped'] += 1
                data['days_stopped'] +=  project.days_plan


        data['pro_porcen'] = data['pro_done'] * 100 / data['len_project'] 
        data['days_total'] = data['days_done'] + data['days_process'] + data['days_stopped']
        data['days_porcen'] = data['days_done'] * 100 / data['days_total'] 

        data['projects_done'] = projects_done
        data['projects_stopped'] = projects_stopped
        data['projects_process'] = projects_process

        return data