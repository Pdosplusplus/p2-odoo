# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Deliverable(models.Model):

    _name = 'agilis.deliverable'

    name = fields.Char(string="Nombre", 
                    required=True,
                    unique=True)

    description = fields.Text(string="Descripcion",
                    required=True)

    type_measure = fields.Many2one(
                    'agilis.measure',
                    ondelete='set null', 
                    string="Tipo de medida",  
                    index=True)

    advances = fields.Integer(string="Numero de Avances",
                    required=True)

    journals_plan = fields.Integer(string="N Jornadas Planificadas")

    journals_exe = fields.Integer(string="N Jornadas Ejecutadas",
                    compute="_journal")

    service_id = fields.Many2one('agilis.service',
                            ondelete='cascade', 
                            string="Servicio")
    
    project_id = fields.Many2one('agilis.project',
                            ondelete='cascade', 
                            string="Proyecto")


    def _journal(self):

        for r in self:

            num = 0
            
            if r.project_id:

                for activity in r.project_id.activity_ids:

                    if activity.deliverable_id.id == r.id:

                        num += activity.journals_exe

            r.journals_exe = num
