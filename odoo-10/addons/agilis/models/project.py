# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, date
from dateutil import rrule

class Project(models.Model):

    _name = 'agilis.project'

    name = fields.Char(string="Nombre del Proyecto", 
                       required=True,
                       unique=True)


    workplan_id = fields.Many2one('agilis.workplan',
                           string="Planificación")

