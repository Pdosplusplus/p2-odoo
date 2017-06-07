# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.addons.agili.common.utils import workDays, daysExe, compareDates

class Activity(models.Model):

    _name = 'agili.activity'

    name = fields.Char(string="Nombre de Actividad", required=True)

    ac_start_date = fields.Date(string="Fecha de inicio", required=True)

    ac_end_date = fields.Date(string="Fecha de Fin", required=True)
   
    ac_days_plan = fields.Integer(string="Dias planificados", 
                                compute='_diasLaborales',
                                store=True)

    ac_days_exe = fields.Integer(string="Dias ejecutados",
                                compute="_daysexe")

    ac_progress = fields.Integer(string="Porcentaje de avance",
                                compute="_progress")

    ac_work_real = fields.Integer(string="Reporte de trabajo real")

    ac_responsible_id = fields.Many2one('res.users',
                            ondelete='set null',
                            string="Responsable", 
                            required=True)

    ac_deliverable_id = fields.Many2one('agili.deliverable',
                         ondelete='cascade', 
                         string="Entregable")

    _sql_constraints = [
        ('name_description_check',
        'CHECK(name != description)',
        "El nombre de la actividad no puede ser la descripción."),

        ('name_unique',
        'UNIQUE(name)',
        "El nombre de la actividad es unica"),

        ('days_valid',
        'CHECK(ac_days_plan > 0)',
        "Los dias planificados tienen que ser mayor a 0"),
        
    ]

    @api.depends('ac_start_date', 'ac_end_date')
    def _diasLaborales(self):
        
        for r in self:

            if r.ac_start_date and r.ac_end_date:

                r.ac_days_plan = workDays(r.ac_start_date, r.ac_end_date)
               
    @api.constrains('ac_days_exe')
    def _check_days_activity(self):

        for r in self:
            
            if r.ac_days_exe > r.ac_days_plan:
                    
                    raise ValidationError('Los dias ejecutados no pueden ser mayor a los planificados')

    @api.onchange('ac_start_date', 'ac_end_date')
    def _check_date(self):

        for r in self:
            
            if r.ac_start_date and r.ac_end_date:

                if compareDates(r.ac_end_date, r.ac_start_date, 'less'):
                    
                    raise ValidationError('La fecha de fin de la actividad no puede ser menor que la fecha de inicio')

    @api.depends('ac_start_date')
    def _daysexe(self):

        for r in self:

            if r.ac_start_date:

                r.ac_days_exe = daysExe(r.ac_start_date)

    @api.depends('ac_days_exe', 'ac_days_plan')
    def _progress(self):

        for r in self:

            if r.ac_days_exe > 0 and r.ac_days_plan > 0:

                r.ac_progress = r.ac_days_exe * 100 / r.ac_days_plan

                if r.ac_progress > 100:

                    r.ac_progress = 100
