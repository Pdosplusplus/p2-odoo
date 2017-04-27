# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions

class Deliverable(models.Model):
    
    _name = 'agili.deliverable'

    name = fields.Char(string="Nombre", 
                       required=True)

    deliverable = fields.Binary(string="Entregable", 
                                attachment=True,
                                required=True)

    de_project_id = fields.Many2one('agili.project',
                                ondelete='cascade', 
                                string="Proyecto", 
                                required=True)

    de_type = fields.Selection([
        ('primer', "Primer nivel"),
        ('segundo', "Segundo nivel"),
    ], string="Nivel", default='primer')
