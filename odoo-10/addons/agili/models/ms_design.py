# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.addons.agili.common.utils import FORMA_DATE, validKey, workDays, sendEmail
from datetime import datetime, date
from dateutil import rrule

class ms_design(models.Model):

    _name = 'agili.ms_design'

    chip_id = fields.Many2one('agili.chip_project',
                         ondelete='cascade', 
                         string="Ficha del Proyecto")

    schedule_id = fields.Many2one('agili.schedule',
                         ondelete='cascade', 
                         string="Cronograma del Proyecto")
