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
                        string="Cooperativa",
                        required=True)

    trimestre_ids = fields.Many2many('agilis.trimestre', 
                        string="Cooperativa",
                        required=True)

    service_ids = fields.One2many('agilis.service', 
                        'project_id', 
                        string="Servicios")

    deliverable_ids = fields.One2many('agilis.deliverable', 
                        'project_id', 
                        string="Entregables")



    _sql_constraints = [
         ('name_unique',
        'UNIQUE(name)',
        "El nombre del proyecto es unico"),

        ('name_description_check',
        'CHECK(name != description)',
        "El nombre del proyecto no puede ser la descripción."),
    ]
