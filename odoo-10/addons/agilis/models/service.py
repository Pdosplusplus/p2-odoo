# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Service(models.Model):

    _name = 'agilis.service'

    name = fields.Char(string="Nombre", 
                    required=True,
                    unique=True)

    description = fields.Text(string="Descripcion",
                    required=True)

    journals = fields.Integer(string="N Jornadas",
                    required=True)

    project_id = fields.Many2one('agilis.project',
                            ondelete='cascade', 
                            string="Proyecto")

    _sql_constraints = [
        ('name_unique',
        'UNIQUE(name)',
        "La cooperativa ya se encuentra registrada"),
    ]