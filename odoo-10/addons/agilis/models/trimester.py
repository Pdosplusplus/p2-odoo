# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Trimestre(models.Model):

    _name = 'agilis.trimestre'

    name = fields.Char(string="Trimestre", 
                    required=True,
                    unique=True)

    date_ini = fields.Date(string="Fecha Inicio",
                    required=True)

    date_end = fields.Date(string="Fecha Fin",
                    required=True)

    _sql_constraints = [
        ('name_unique',
        'UNIQUE(name)',
        "El trimestre ya se encuentra registrado"),
    ]