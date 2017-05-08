# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Project(models.Model):

    _name = 'agili.project'

    name = fields.Char(string="Nombre del Proyecto", required=True)

    description = fields.Text(string="Descripción")

    start_date = fields.Date(string="Fecha de inicio", required=True)

    end_date = fields.Date(string="Fecha de Fin", required=True)

    hour_man = fields.Integer(string="H.H Planificadas", 
                              help="Horas hombres planificadas")

    hour_man_exe = fields.Integer(string="H.H Ejecutadas",
                                  compute='_hour_exec',
                                  help="Horas hombres ejecutadas")

    responsible_ids = fields.Many2many('res.users', 
                                        string="Responsables",
                                        required=True)


    porcen_project = fields.Float(string="Avance del proyecto",
                                  compute='_porcent_project')

    activity_ids = fields.One2many(
        'agili.activity', 'ac_project_id', string="Actividades")

    activities_count = fields.Integer(string="Numero de actividades", 
                                    compute='_get_activities_count', 
                                    store=True)

    deliverable_ids = fields.One2many(
        'agili.deliverable', 'de_project_id', string="Entregables")


    _sql_constraints = [
        ('name_description_check',
        'CHECK(name != description)',
        "El nombre del proyecto no puede ser la descripción."),

        ('name_unique',
        'UNIQUE(name)',
        "El nombre del proyecto es unico"),

        ('hour_valid',
        'CHECK(hour_man > 0)',
        "Las horas hombre tienen que ser mayor a 0"),
    ]

    state = fields.Selection([
        ('process', "En proceso"),
        ('stopped', "Detenido"),
        ('done', "Terminado"),
    ], string="Estado", default='process')

    @api.multi
    def action_process(self):
        self.state = 'process'

    @api.multi
    def action_stopped(self):
        self.state = 'stopped'

    @api.multi
    def action_done(self):
        self.state = 'done'

    #Función para calcular cuantas acitvidades hay en proyecto
    @api.depends('activity_ids')
    def _get_activities_count(self):
        for r in self:
            r.activities_count = len(r.activity_ids)
            print r.activities_count

    #Funcion para calcular las horas ejecutadas
    @api.depends('activity_ids')
    def _hour_exec(self):
        for r in self:
            if not r.activity_ids:

                r.hour_man_exe = 0
            
            else:

                hour_exe = 0

                for act in r.activity_ids:
                    
                    if act.ac_state == 'done':

                        hour_exe += act.ac_hour_man_exe

                r.hour_man_exe = hour_exe

    #Funcion para calcular el porcentaje ejecutado de un proyecto
    @api.depends('activity_ids')
    def _porcent_project(self):
        for r in self:
            if not r.activity_ids:

                r.porcen_project = 0.0
            
            else:

                hour_done = 0


                for act in r.activity_ids:
                    
                    if act.ac_state == 'done':

                        hour_done += act.ac_hour_man

                r.porcen_project = 100 * hour_done / r.hour_man

    @api.constrains('activity_ids')
    def _check_hour_activity(self):

        for r in self:
            
            hour_total = 0

            for act in r.activity_ids:
                
                hour_total += act.ac_hour_man

                if act.ac_hour_man > r.hour_man or hour_total > r.hour_man:
                    
                    raise ValidationError('Las horas hombre declaradas sobrepasan a las horas hombre del proyecto')

    @api.model
    def print_report(self):

        context = self.env.context
    
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'agili.report_project_general',
            'context': context,
        }

def validKey(array, key):

    try:

        print "No es posible"
        return array[key]

    except KeyError as e:
        
        print e

        return 0

class report_project_general(models.AbstractModel):
    _name = 'report.agili.report_project_general'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('agili.report_project_general')
        projects = self.env['agili.project'].search([('hour_man','>=', 0)])
        
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

        data['hour_done'] = 0
        data['hour_process'] = 0 
        data['hour_stopped'] = 0

        data['pro_porcen'] = 0
        data['hour_total'] = 0
        data['hour_porcen'] = 0

        projects = self.env['agili.project'].search([('hour_man','>=', 0)])

        data['len_project'] = len(projects)

        projects_done = []
        projects_stopped = []
        projects_process = []

        for project in projects:

            if project.state == 'done':

                p = {}
                p['name'] = project.name
                projects_done.append(p)

                data['pro_done'] += 1
                data['hour_done'] += project.hour_man

            if project.state == 'process':

                p = {}
                responsibles = []

                p['name'] = project.name


                for respon in project.responsible_ids:

                    r = {}
                    r['name'] = respon.name
                    r['hour_man'] = 0
                    r['hour_man_exe'] = 0

                    for activity in project.activity_ids:

                        if respon.name == activity.ac_responsible_id.name:
                        
                            r['hour_man'] = validKey(activity, "ac_hour_man")

                            r['hour_man_exe'] += validKey(activity, "ac_hour_man_exe")


                    responsibles.append(r)

                p['responsibles'] = responsibles


                projects_process.append(p)

                data['pro_process'] += 1
                data['hour_process'] +=  project.hour_man


            if project.state == 'stopped':

                p = {}
                p['name'] = project.name
                projects_stopped.append(p)

                data['pro_stopped'] += 1
                data['hour_stopped'] +=  project.hour_man


        data['pro_porcen'] = data['pro_done'] * 100 / data['len_project'] 
        data['hour_total'] = data['hour_done'] + data['hour_process'] + data['hour_stopped']
        data['hour_porcen'] = data['hour_done'] * 100 / data['hour_total'] 

        data['projects_done'] = projects_done
        data['projects_stopped'] = projects_stopped
        data['projects_process'] = projects_process

        return data