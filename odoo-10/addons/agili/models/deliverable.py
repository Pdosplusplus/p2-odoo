# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo.addons.agili.common.utils import FORMA_DATE, compareDates, DAYS_LESS, DAYS_HIGHER, validKey, workDays, daysExe

higher = ''
less = ''

class Deliverable(models.Model):

    _name = 'agili.deliverable'

    name = fields.Char(string="Nombre", 
                   required=True)

    dl_unit_measure = fields.Char(string="Unidad de medida",
                                required=True)
    
    dl_num_trimestre = fields.Integer(string="N de entregras por trimestre")

    dl_num_talent = fields.Integer(string="Talentos Proyectados")

    dl_num_journeys = fields.Integer(string="Jornadas Proyectadas")

    dl_amount = fields.Float(string="Inversion")

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
