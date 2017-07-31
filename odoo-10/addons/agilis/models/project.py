# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.addons.agilis.common.utils import FORMA_DATE, validKey, workDays, sendEmail, daysExe
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

    _sql_constraints = [
         ('name_unique',
        'UNIQUE(name)',
        "El nombre del proyecto es unico"),

        ('name_description_check',
        'CHECK(name != description)',
        "El nombre del proyecto no puede ser la descripción."),
    ]
