# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Deliverable(models.Model):

    _name = 'agilis.deliverable'

    name = fields.Char(string="Nombre", 
                    required=True)

    description = fields.Text(string="Descripcion",
                    required=True)

    journals = fields.Integer(string="N Jornadas",
                    required=True)

    type_measure = fields.Many2one(
                    'agilis.measure',
                    ondelete='set null', 
                    string="Tipo de medida",  
                    index=True)

    num_advances = fields.Integer(string="Numero de Avances",
                    required=True)

    num_journals = fields.Integer(string="Numero de Jornadas",
                    required=True)

    service_id = fields.Many2one('agilis.service',
                            ondelete='cascade', 
                            string="Servicio")

    project_id = fields.Many2one('agilis.project',
                            ondelete='cascade', 
                            string="Proyecto")