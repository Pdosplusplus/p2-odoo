# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions

class Deliverable(models.Model):

    _name = 'agili.deliverable'

    name_dl = fields.Char(string="Nombre", 
                   required=True)

    dl_start_date = fields.Date(string="Fecha de inicio")

    dl_end_date = fields.Date(string="Fecha de Fin")

    dl_days_plan = fields.Integer(string="Dias planificados", 
                                    compute='_diasLaborales',
                                    store=True)

    dl_days_exe = fields.Integer(string="Dias ejecutados")

    dl_workplan_id = fields.Many2one('agili.workplan',
                         ondelete='cascade', 
                         string="Plan de trabajo")

    deliverable_ids = fields.One2many('agili.deliverable', 
                        'dl_milestone_id', 
                        string="Entregables")

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

    

    @api.depends('dl_start_date', 'dl_end_date')
    def _diasLaborales(self):
        
        for r in self:

            if r.dl_start_date and r.dl_end_date:

                r.dl_days_plan = workDays(r.dl_start_date, r.dl_end_date)

