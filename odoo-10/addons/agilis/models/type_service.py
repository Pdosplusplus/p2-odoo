# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TypeService(models.Model):

    _name = 'agilis.type_service'

    name = fields.Char(string="Nombre", 
                    required=True,
                    unique=True)

    _sql_constraints = [
        ('name_unique',
        'UNIQUE(name)',
        "El servicio ya se encuentra registrado"),
    ]
