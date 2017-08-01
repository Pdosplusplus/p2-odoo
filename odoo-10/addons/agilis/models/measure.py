# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Measure(models.Model):

    _name = 'agilis.measure'

    name = fields.Char(string="Nombre", 
                    required=True,
                    unique=True)

    _sql_constraints = [
         ('name_unique',
        'UNIQUE(name)',
        "El tipo de documento ya esta registrado"),
    ]
