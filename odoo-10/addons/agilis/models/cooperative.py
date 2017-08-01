# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Cooperative(models.Model):

    _name = 'agilis.cooperative'

    name = fields.Char(string="Nombre de la cooperativa", 
                       required=True,
                       unique=True)

    cooperativista_ids = fields.Many2many('res.users', 
                      string="Cooperativista")

    _sql_constraints = [
        ('name_unique',
        'UNIQUE(name)',
        "La cooperativa ya se encuentra registrada"),
    ]