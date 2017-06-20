# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo.addons.agili.common.utils import FORMA_DATE, compareDates, DAYS_LESS, DAYS_HIGHER, validKey, workDays, daysExe

higher = ''
less = ''

class Deliverable(models.Model):

    _name = 'agili.deliverable'

    name = fields.Char(string="Nombre", 
                   required=True)

    dl_start_date = fields.Date(string="Fecha de inicio")

    dl_end_date = fields.Date(string="Fecha de Fin")

    dl_days_plan = fields.Integer(string="Dias planificados", 
                                  compute='_diasLaborales')

    dl_days_exe = fields.Integer(string="Dias ejecutados",
                                 compute="_daysexe")

    dl_progress = fields.Integer(string="Porcentaje de avance")

    dl_work_real = fields.Integer(string="Reporte de avance real en dias")

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

    
   