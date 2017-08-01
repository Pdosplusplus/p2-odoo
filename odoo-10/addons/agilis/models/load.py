# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Load(models.Model):

    _name = 'agilis.load'

    deliverable_id = fields.Many2one('agilis.deliverable',
                        string="Entregable",
                        ondelete='cascade',
                        required=True )

    cooperative_id = fields.Many2one('agilis.cooperative',
                        string="Cooperativa",
                        ondelete='cascade', 
                        required=True)

    cooperativista_id = fields.Many2one('res.users', 
                        string="Cooperativista",
                        ondelete='cascade',
                        required=True)

    journals = fields.Integer(string="N Jornadas",
                        required=True)

    project_id = fields.Many2one('agilis.project',
                        ondelete='cascade', 
                        string="Proyecto")