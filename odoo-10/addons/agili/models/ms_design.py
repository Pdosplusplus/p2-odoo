# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.addons.agili.common.utils import FORMA_DATE, validKey, workDays, sendEmail
from datetime import datetime, date
from dateutil import rrule

class ms_design(models.Model):

    _name = 'agili.ms_design'

    deliverable = fields.Char(string="Entregable", 
                        required=True,
                        unique=True)

    ds_activity_ids = fields.One2many('agili.activity', 
                        'ac_desing_id', 
                        string="Actividades")