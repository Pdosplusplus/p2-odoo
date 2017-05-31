# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions

class Deliverable(models.Model):
    
    _name = 'agili.deliverable'

    name = fields.Char(string="Nombre", 
                       required=True)

    deliverable = fields.Binary(string="Entregable", 
                                attachment=True,
                                required=True)
