# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Bank(models.Model):

    _name = 'sigesalud.bank'

    name = fields.Char(string="Nombre del Banco", 
                       required=True)

    _sql_constraints = [
        ('name_unique',
        'UNIQUE(name)',
        "El banco ya esta registrado"),
    ]