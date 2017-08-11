# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Policy(models.Model):
    
    _name = 'sigesalud.policy'

    name = fields.Char(string="Nombre", 
                        required=True)

    sum_assured = fields.Float(string="Suma asegurada",
                        required=True)

    range_ids = fields.Many2many('sigesalud.range', 
                        string="Rangos")
