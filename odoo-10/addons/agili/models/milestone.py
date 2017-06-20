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

    ms_start_date = fields.Date(string="Fecha de inicio",
                                compute="_daystart")

    ms_end_date = fields.Date(string="Fecha de Fin",
                              compute="_dayend")

    ms_days_plan = fields.Integer(string="Dias planificados",
                                  compute="_diasLaborales")

    ms_days_exe = fields.Integer(string="Dias ejecutados",
                                 compute='_daysexe')

    ms_progress = fields.Integer(string="Porcentaje de avance")

    ms_work_real = fields.Integer(string="Reporte de avance real en dias")

    ms_project_id = fields.Many2one('agili.project',
                         ondelete='cascade', 
                         string="Proyecto")

    ms_responsible_id = fields.Many2one('res.users',
                            ondelete='set null',
                            string="Responsable", 
                            required=True)

    #Function to calculate the date of init
    def _daystart(self):
        
        less = DAYS_LESS

        for r in self:

            deliverables = self.env['agili.deliverable'].search([('dl_milestone_id','=', r.id)])

            if deliverables:

                for deliverable in deliverables:

                    if deliverable.dl_start_date:

                        if less == '':
                                
                            less = DAYS_LESS

                        if compareDates(deliverable.dl_start_date, less, 'less'):

                            less = deliverable.dl_start_date

            else:

                less = ''

        r.ms_start_date = less

    #Function to calculate the date of finish
    def _dayend(self):
        
        higher = DAYS_HIGHER

        for r in self:

            deliverables = self.env['agili.deliverable'].search([('dl_milestone_id','=', r.id)])

            if deliverables:

                for deliverable in deliverables:

                    if deliverable.dl_end_date:

                        if higher == '':

                            higher = DAYS_HIGHER

                        if compareDates(deliverable.dl_end_date, higher, 'higher'):

                            higher = deliverable.dl_end_date

            else:

                higher = ''

            r.ms_end_date = higher
    
    @api.depends('ms_start_date')
    def _daysexe(self):

        for r in self:

            if r.ms_start_date != False and r.ms_end_date != False:

                r.ms_days_exe = daysExe(r.ms_start_date, r.ms_end_date)

    @api.depends('ms_start_date', 'ms_end_date')
    def _diasLaborales(self):
        
        for r in self:

            if r.ms_start_date != False and r.ms_end_date != False:

                r.ms_days_plan = workDays(r.ms_start_date, r.ms_end_date)
                

    """
    @api.depends('deliverable_ids')
    def _progress(self):
        
        for r in self:
                
            deliverables = 0
            total_progress = 0

            if r.deliverable_ids:

                for deliverable in r.deliverable_ids:

                    total_progress += deliverable.dl_progress 
                    deliverables += 1

                if deliverables > 0:

                    r.ms_progress = total_progress / deliverables

                else:

                    r.ms_progress = 0

    @api.depends('deliverable_ids')
    def _workreal(self):
        
        for r in self:
                
            total_workreal = 0

            if r.deliverable_ids:

                for deliverable in r.deliverable_ids:

                    total_workreal += deliverable.dl_work_real 

                r.ms_work_real = total_workreal 
    """