# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Activity(models.Model):

    _name = 'agili.activity'

    name = fields.Char(string="Nombre de Actividad", required=True)

    ac_type = fields.Selection([
        ('primer', "Primer nivel"),
        ('segundo', "Segundo nivel"),
    ], string="Nivel", default='primer')
    
    ac_start_date = fields.Date(string="Fecha de inicio", required=True)

    ac_end_date = fields.Date(string="Fecha de Fin", required=True)
   
    objetive = fields.Char(string="Objetivo", required=True)
    
    description = fields.Text(string="Descripción")

    result = fields.Text(string="Resultado")

    ac_hour_man = fields.Integer(string="Horas hombres", required=True)

    ac_responsible_id = fields.Many2one('res.users',
    ondelete='set null', string="Responsable", required=True, index=True)

    ac_project_id = fields.Many2one('agili.project',
        ondelete='cascade', string="Proyecto", required=True)

    _sql_constraints = [
        ('name_description_check',
        'CHECK(name != description)',
        "El nombre de la actividad no puede ser la descripción."),

        ('name_unique',
        'UNIQUE(name)',
        "El nombre de la actividad es unica"),

        ('hour_valid',
        'CHECK(ac_hour_man > 0)',
        "Las horas hombre tienen que ser mayor a 0"),
        
    ]

    ac_state = fields.Selection([
        ('process', "En proceso"),
        ('stopped', "Detenida"),
        ('done', "Terminada"),
    ], string="Estado", default='process')

    @api.multi
    def action_process(self):
        self.ac_state = 'process'

    @api.multi
    def action_stopped(self):
        self.ac_state = 'stopped'

    @api.multi
    def action_done(self):
        self.ac_state = 'done'
