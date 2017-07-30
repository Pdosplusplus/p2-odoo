# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Exam(models.Model):
    
    _name = 'sigesalud.exam'

    name = fields.Char(string="Nombre ", 
                        required=True)

    cost = fields.Char(string="Costo del examen",
                        required=True)

    support = fields.Binary(string="Soporte", 
                        attachment=True)

    event_id = fields.Many2one('sigesalud.event',
                            ondelete='cascade', 
                            string="Evento")