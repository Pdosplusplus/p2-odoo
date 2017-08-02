# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Advance(models.Model):

    _name = 'agilis.advance'

    activity_id = fields.Many2one('agilis.activity',
                            string="Actividad",
                            ondelete='cascade',
                            required=True )

    date = fields.Date(string="Fecha de reporte", 
                            required=True)

    description = fields.Text(string="Descripcion", 
                            required=True)

    percentage = fields.Char(string="% Avance")

    talents = fields.Integer(string="N Talento")

    journals = fields.Integer(string="N de Jornadas")

    project_id = fields.Many2one('agilis.project',
                            ondelete='cascade', 
                            string="Proyecto")