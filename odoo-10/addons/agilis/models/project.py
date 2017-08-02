# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, date

class Project(models.Model):

    _name = 'agilis.project'

    name = fields.Char(string="Nombre del Proyecto", 
                       required=True,
                       unique=True)

    description = fields.Text(string="Descripción")

    value_journal = fields.Float(string="Valor",
                        required=True)

    cooperative_ids = fields.Many2many('agilis.cooperative', 
                        string="Cooperativa")

    trimestre_ids = fields.Many2many('agilis.trimestre', 
                        string="Cooperativa")

    service_ids = fields.One2many('agilis.service', 
                        'project_id', 
                        string="Servicios")

    deliverable_ids = fields.One2many('agilis.deliverable', 
                        'project_id', 
                        string="Entregables")

    load_ids = fields.One2many('agilis.load', 
                        'project_id', 
                        string="Entregables")

    activity_ids = fields.One2many('agilis.activity', 
                        'project_id', 
                        string="Actividades")

    advance_ids = fields.One2many('agilis.advance', 
                        'project_id', 
                        string="Avance")

    _sql_constraints = [
         ('name_unique',
        'UNIQUE(name)',
        "El nombre del proyecto es unico"),

        ('name_description_check',
        'CHECK(name != description)',
        "El nombre del proyecto no puede ser la descripción."),
    ]
