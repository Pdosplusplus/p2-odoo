# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Disease(models.Model):

    _name = 'sigesalud.expedient'

    name = fields.Char(string="Nombre", 
                       required=True)

    pathology = fields.Char(string="Patalogia", 
                       required=True)

    expedient_id = fields.Many2one('sigesalud.expedient',
                         ondelete='cascade', 
                         string="Expediente")

    beneficiary_id = fields.Many2one('sigesalud.expedient',
                         ondelete='cascade', 
                         string="Expediente")

