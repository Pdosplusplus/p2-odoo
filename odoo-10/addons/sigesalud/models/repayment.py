# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Repayment(models.Model):
    
    _name = 'sigesalud.repayment'

    date = fields.Date(string="Fecha ", 
                        required=True)

    document_ids = fields.One2many('sigesalud.document', 
                        'repayment_id', 
                        string="Documentos")

    expedient_id = fields.Many2one('sigesalud.expedient',
                         ondelete='cascade', 
                         string="Expediente")
