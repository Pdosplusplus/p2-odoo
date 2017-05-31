# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.addons.agili.common.utils import FORMA_DATE, validKey, workDays, sendEmail
from datetime import datetime, date
from dateutil import rrule

class chip_project(models.Model):

    _name = 'agili.chip_project'

    cp_activity_ids = fields.One2many('agili.activity', 
                        'ac_chip_id', 
                        string="Actividades")