# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Range(models.Model):
    
    _name = 'sigesalud.range'

    name = fields.Char(string="Rango", 
                        required=True)
    
    population = fields.Selection([
        ('Hijos y hermanos', "Hijos y hermanos"),
        ('titular o beneficiario', "titular o beneficiario"),
    ], string="Poblacion", required=True)

    bounty = fields.Float(string="Prima de Movimiento",
                        required=True)
