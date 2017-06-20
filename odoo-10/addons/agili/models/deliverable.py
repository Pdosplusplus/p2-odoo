# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo.addons.agili.common.utils import FORMA_DATE, compareDates, DAYS_LESS, DAYS_HIGHER, validKey, workDays, daysExe

higher = ''
less = ''

class Deliverable(models.Model):

    _name = 'agili.deliverable'

    name = fields.Char(string="Nombre", 
                   required=True)

    dl_start_date = fields.Date(string="Fecha de inicio",
                                compute='_daystart')

    dl_end_date = fields.Date(string="Fecha de Fin",
                              compute="_dayend")

    dl_days_plan = fields.Integer(string="Dias planificados", 
                                  compute='_diasLaborales')

    dl_days_exe = fields.Integer(string="Dias ejecutados",
                                 compute="_daysexe")

    dl_progress = fields.Integer(string="Porcentaje de avance",
                                 compute="_progress")

    dl_work_real = fields.Integer(string="Reporte de avance real en dias",
                                 compute="_workreal")

    dl_project_id = fields.Many2one('agili.project',
                         ondelete='cascade', 
                         string="Proyecto")

    dl_milestone_id = fields.Many2one('agili.milestone',
                     ondelete='cascade',
                     required=True, 
                     string="Hito")

    dl_responsible_id = fields.Many2one('res.users',
                            ondelete='set null',
                            string="Responsable", 
                            required=True)

    def _daystart(self):
        
        less = DAYS_LESS

        for r in self:

            activities = self.env['agili.activity'].search([('ac_deliverable_id','>=', r.id)])

            if activities:

                for activity in activities:

                    if activity.ac_start_date:

                        if less == '':
                                
                            less = DAYS_LESS

                        if compareDates(activity.ac_start_date, less, 'less'):

                            less = activity.ac_start_date

            else:

                less = ''

        r.dl_start_date = less

    def _dayend(self):
        
        higher = DAYS_HIGHER

        for r in self:

            activities = self.env['agili.activity'].search([('ac_deliverable_id','>=', r.id)])

            if activities:

                for activity in activities:

                    if activity.ac_end_date:

                        if higher == '':

                            higher = DAYS_HIGHER

                        if compareDates(activity.ac_end_date, higher, 'higher'):

                            higher = activity.ac_end_date

            else:

                higher = ''

            r.dl_end_date = higher

    @api.depends('dl_start_date', 'dl_end_date')
    def _diasLaborales(self):
        
        for r in self:

            if r.dl_start_date != False and r.dl_end_date != False:

                r.dl_days_plan = workDays(r.dl_start_date, r.dl_end_date)


    @api.depends('dl_start_date', 'dl_end_date')
    def _daysexe(self):

        for r in self:

            if r.dl_start_date != False and r.dl_end_date != False:

                r.dl_days_exe = daysExe(r.dl_start_date, r.dl_end_date)

    def _progress(self):
        
        for r in self:
                
            activities = self.env['agili.activity'].search([('ac_deliverable_id','>=', r.id)])

            activity_sum = 0
            total_progress = 0

            if activities:

                for activity in activities:

                    total_progress += activity.ac_progress 
                    activity_sum += 1

                if activity_sum > 0:

                    r.dl_progress = total_progress / activity_sum

    def _workreal(self):
        
        for r in self:
            
            activities = self.env['agili.activity'].search([('ac_deliverable_id','>=', r.id)])
            total_workreal = 0

            if activities:

                for activity in activities:

                    total_workreal += activity.ac_work_real 

                r.dl_work_real = total_workreal
