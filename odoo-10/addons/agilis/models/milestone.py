# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.addons.agilis.common.utils import FORMA_DATE, compareDates, DAYS_LESS, DAYS_HIGHER, validKey, workDays, daysExe
from datetime import datetime, date
from dateutil import rrule

less = ''
higher = ''

class milestone(models.Model):

    _name = 'agilis.milestone'

    name = fields.Char(string="Nombre",
    					  required=True)

    ms_description = fields.Text(string="Descripción")

    ms_amount = fields.Float(string="Monto del Servicio")

    ms_project_id = fields.Many2one('agilis.project',
                         ondelete='cascade', 
                         string="Proyecto")

    ms_responsible_id = fields.Many2one('res.users',
                            ondelete='set null',
                            string="Responsable", 
                            required=True)