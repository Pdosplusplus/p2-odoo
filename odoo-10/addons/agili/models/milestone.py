# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.addons.agili.common.utils import FORMA_DATE, compareDates, DAYS_LESS, DAYS_HIGHER, validKey, workDays, sendEmail
from datetime import datetime, date
from dateutil import rrule

less = ''
higher = ''

class milestone(models.Model):

    _name = 'agili.milestone'

    name_ms = fields.Char(string="Hito del proyecto",
    					  required=True)

    ms_start_date = fields.Date(string="Fecha de inicio",
                                compute='_daystart')

    ms_end_date = fields.Date(string="Fecha de Fin",
                              compute='_dayend')

    ms_days_plan = fields.Integer(string="Dias planificados", 
                                    compute='_diasLaborales',
                                    store=True)

    ms_days_exe = fields.Integer(string="Dias ejecutados")

    ms_workplan_id = fields.Many2one('agili.workplan',
                         ondelete='cascade', 
                         string="Plan de trabajo")

    deliverable_ids = fields.One2many('agili.deliverable', 
                        'dl_milestone_id', 
                        string="Entregables")

    ms_responsible_id = fields.Many2one('res.users',
                            ondelete='set null',
                            string="Responsable", 
                            required=True)


    @api.depends('deliverable_ids')
    def _daystart(self):
        
        less = DAYS_LESS

        for r in self:

            for deliverable in r.deliverable_ids:

                if deliverable.dl_start_date:

                    if compareDates(deliverable.dl_start_date, less, 'less'):

                        less = deliverable.dl_start_date

        r.ms_start_date = less

    @api.depends('deliverable_ids')
    def _dayend(self):
        
        higher = DAYS_HIGHER

        for r in self:

            for deliverable in r.deliverable_ids:

                print str(deliverable.dl_end_date)

                if deliverable.dl_end_date:

                    if compareDates(deliverable.dl_end_date, higher, 'higher'):

                        higher = deliverable.dl_end_date

        r.ms_end_date = higher


    @api.depends('ms_start_date', 'ms_end_date')
    def _diasLaborales(self):
        
        for r in self:

            if r.ms_start_date and r.ms_end_date:

                r.ms_days_plan = workDays(r.ms_start_date, r.ms_end_date)
                
