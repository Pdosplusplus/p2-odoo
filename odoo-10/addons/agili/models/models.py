# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api, exceptions

class Project(models.Model):

    _name = 'agili.project'

    name = fields.Char(string="Nombre del Proyecto", required=True)

    description = fields.Text(string="Descripción")

    start_date = fields.Date(string="Fecha de inicio", required=True)

    end_date = fields.Date(string="Fecha de Fin", required=True)

    hour_man = fields.Integer(string="Horas hombres")

    responsible_id = fields.Many2one('res.users',
    ondelete='set null', string="Responsable", index=True)

    porcen_project = fields.Float(string="Avance del proyecto")

    activity_ids = fields.One2many(
        'agili.activity', 'project_id', string="Actividades")

    activities_count = fields.Integer(string="Numero de actividades", 
        compute='_get_activities_count', store=True)

    _sql_constraints = [
        ('name_description_check',
        'CHECK(name != description)',
        "El nombre del proyecto no puede ser la descripción."),

        ('name_unique',
        'UNIQUE(name)',
        "El nombre del proyecto es unico"),
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

class Activity(models.Model):

    _name = 'agili.activity'

    name = fields.Char(string="Nombre de Actividad", required=True)
    
    ac_start_date = fields.Date(string="Fecha de inicio", required=True)

    ac_end_date = fields.Date(string="Fecha de Fin", required=True)
   
    objetive = fields.Char(string="Objetivo", required=True)
    
    description = fields.Text(string="Descripción")

    result = fields.Text(string="Resultado")

    ac_hour_man = fields.Integer(string="Horas hombres")

    ac_responsible_id = fields.Many2one('res.users',
    ondelete='set null', string="Responsable", index=True)

    project_id = fields.Many2one('agili.project',
        ondelete='cascade', string="Proyecto", required=True)

