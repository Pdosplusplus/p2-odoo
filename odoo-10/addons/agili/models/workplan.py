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

    wk_progress = fields.Integer(string="Avance del plan de trabajo",
    							compute="_progress")

    wk_work_real = fields.Integer(string="Reporte de avance real",
                                 compute="_workreal")

    milestone_ids = fields.One2many('agili.milestone', 
                        'ms_workplan_id', 
                        string="Hitos")


    @api.depends('milestone_ids')
    def _progress(self):
        
        for r in self:
                
            milestones = 0
            total_progress = 0

            if r.milestone_ids:

                for milestone in r.milestone_ids:

                    total_progress += milestone.ms_progress 
                    milestones += 1

                if milestones > 0:

                    r.wk_progress = total_progress / milestones

                else:

                    r.wk_progress = 0

    @api.depends('milestone_ids')
    def _workreal(self):
        
        for r in self:
                
            total_workreal = 0

            if r.milestone_ids:

                for milestone in r.milestone_ids:

                    total_workreal += milestone.ms_work_real 
                 

                r.wk_work_real = total_workreal
