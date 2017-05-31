# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.addons.agili.common.utils import FORMA_DATE, validKey, workDays, sendEmail
from datetime import datetime, date
from dateutil import rrule

class schedule(models.Model):

    _name = 'agili.schedule'

    sc_activity_ids = fields.One2many('agili.activity', 
                        'ac_schedule_id', 
                        string="Actividades")