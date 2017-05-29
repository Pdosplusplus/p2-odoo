# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, date
from dateutil import rrule

class Workplan(models.Model):

    _name = 'agilis.workplan'

    name = fields.Char(string="Plan de trabajo", 
                       required=True,
                       unique=True)


    workplan_id = fields.Many2one('agilis.project',
        					string="Proyecto")