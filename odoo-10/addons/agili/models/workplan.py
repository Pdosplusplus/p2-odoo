# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.addons.agili.common.utils import FORMA_DATE, validKey, workDays, sendEmail
from datetime import datetime, date
from dateutil import rrule

class Workplan(models.Model):

    _name = 'agili.workplan'

    name = fields.Char(string="Plan de trabajo", 
                       required=True,
                       unique=True)

    milestone_ids = fields.One2many('agili.milestone', 
                        'ms_workplan_id', 
                        string="Hitos")