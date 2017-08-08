# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Activity(models.Model):

    _name = 'agilis.activity'

    deliverable_id = fields.Many2one('agilis.deliverable',
                        string="Entregable",
                        ondelete='cascade',
                        required=True )

    name = fields.Char(string="Nombre de Actividad", 
                        required=True)

    cooperativista_ids = fields.Many2many('res.users', 
                        string="Responsables",
                        required=True)

    journals_plan = fields.Integer(string="N Jornadas Planificadas")

    journals_exe = fields.Integer(string="N Jornadas Ejecutadas",
                    compute="_journal")

    project_id = fields.Many2one('agilis.project',
                        ondelete='cascade', 
                        string="Proyecto")

    def _journal(self):

        for r in self:

            num = 0
            
            if r.project_id:

                for advance in r.project_id.advance_ids:

                    if advance.activity_id.id == r.id:

                        num += advance.journals

            r.journals_exe = num

