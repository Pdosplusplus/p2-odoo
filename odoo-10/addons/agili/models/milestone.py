# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.addons.agili.common.utils import FORMA_DATE, compareDates, DAYS_LESS, DAYS_HIGHER, validKey, workDays, daysExe
from datetime import datetime, date
from dateutil import rrule

less = ''
higher = ''

class milestone(models.Model):

    _name = 'agili.milestone'

    name = fields.Char(string="Nombre",
    					  required=True)

    ms_amount = fields.Float(string="Monto del Servicio")

    ms_project_id = fields.Many2one('agili.project',
                         ondelete='cascade', 
                         string="Proyecto")

    ms_responsible_id = fields.Many2one('res.users',
                            ondelete='set null',
                            string="Responsable", 
                            required=True)