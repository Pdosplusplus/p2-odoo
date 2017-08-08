# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Service(models.Model):

    _name = 'agilis.service'

    type_service = fields.Many2one(
                    'agilis.type_service',
                    ondelete='set null', 
                    string="Servicio",  
                    index=True)

    description = fields.Text(string="Descripcion",
                    required=True)

    journals_plan = fields.Integer(string="N Jornadas Planificadas")

    journals_exe = fields.Integer(string="N Jornadas Ejecutadas",
                    compute="_journal")

    project_id = fields.Many2one('agilis.project',
                            ondelete='cascade', 
                            string="Proyecto")

    _sql_constraints = [
        ('name_unique',
        'UNIQUE(name)',
        "La cooperativa ya se encuentra registrada"),
    ]

    def _journal(self):

        for r in self:

            num = 0
            
            if r.project_id:

                for deliverable in r.project_id.deliverable_ids:

                    if deliverable.type_service == r.type_service:

                        num += deliverable.journals_exe

            r.journals_exe = num