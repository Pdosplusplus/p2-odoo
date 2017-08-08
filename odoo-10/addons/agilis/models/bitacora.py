# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date

class Bitacora(models.Model):

    _name = 'agilis.bitacora'

    activity_id = fields.Many2one('agilis.activity',
                            string="Actividad",
                            ondelete='cascade',
                            required=True )

    date = fields.Date(string="Fecha de reporte", 
                            required=True,
                            default= datetime.now().date())

    description = fields.Text(string="Descripcion", 
                            required=True)

    journals = fields.Integer(string="N de Jornadas")
