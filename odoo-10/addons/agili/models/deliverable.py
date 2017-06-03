# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo.addons.agili.common.utils import FORMA_DATE, compareDates, DAYS_LESS, DAYS_HIGHER, validKey, workDays


higher = ''
less = ''

class Deliverable(models.Model):

    _name = 'agili.deliverable'

    name_dl = fields.Char(string="Nombre", 
                   required=True)

    dl_start_date = fields.Date(string="Fecha de inicio",
                                compute='_daystart')

    dl_end_date = fields.Date(string="Fecha de Fin",
                              compute='_dayend')

    dl_days_plan = fields.Integer(string="Dias planificados", 
                                  compute='_diasLaborales')

    dl_days_exe = fields.Integer(string="Dias ejecutados",
                                 compute="_daysexe")

    dl_progress = fields.Integer(string="Dias ejecutados",
                                 compute="_progress")

    dl_workplan_id = fields.Many2one('agili.workplan',
                         ondelete='cascade', 
                         string="Plan de trabajo")

    dl_responsible_id = fields.Many2one('res.users',
                            ondelete='set null',
                            string="Responsable", 
                            required=True)

    dl_milestone_id = fields.Many2one('agili.milestone',
                     ondelete='cascade', 
                     string="Hito")

    dl_activity_ids = fields.One2many('agili.activity',
                    'ac_deliverable_id', 
                    string="Actividades")

    
    @api.depends('dl_activity_ids')
    def _daystart(self):
        
        less = DAYS_LESS

        for r in self:

            if r.dl_activity_ids:

                for activity in r.dl_activity_ids:

                    if activity.ac_start_date:

                        if compareDates(activity.ac_start_date, less, 'less'):

                            less = activity.ac_start_date

        r.dl_start_date = less

    @api.depends('dl_activity_ids')
    def _dayend(self):
        
        higher = DAYS_HIGHER

        for r in self:

            if r.dl_activity_ids:
                
                for activity in r.dl_activity_ids:

                    if activity.ac_end_date:

                        if compareDates(activity.ac_end_date, higher, 'higher'):

                            higher = activity.ac_end_date

        r.dl_end_date = higher

    @api.depends('dl_start_date', 'dl_end_date')
    def _diasLaborales(self):
        
        for r in self:

            if r.dl_start_date and r.dl_end_date:

                r.dl_days_plan = workDays(r.dl_start_date, r.dl_end_date)


    @api.depends('dl_activity_ids')
    def _daysexe(self):
        
        higher = DAYS_HIGHER

        for r in self:
                
            sum_day = 0

            if r.dl_activity_ids:

                for activity in r.dl_activity_ids:

                    if activity.ac_days_exe:

                        sum_day += activity.ac_days_exe


            r.dl_days_exe = sum_day


