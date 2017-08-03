# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Repayment(models.Model):
    
    _name = 'sigesalud.repayment'

    date = fields.Date(string="Fecha de entrega a la compania de seguros", 
                        required=True)

    state = fields.Selection([
        ('En Proceso', "En Proceso"),
        ('Ejecutado', "Ejecutado"),
        ('Cancelado', "Cancelado"),
    ], default='En Proceso', string="Estado")

    event_id = fields.Many2one('sigesalud.event',
                         ondelete='cascade', 
                         string="Evento")

    document_ids = fields.One2many('sigesalud.document', 
                        'repayment_id', 
                        string="Documentos")

    expedient_id = fields.Many2one('sigesalud.expedient',
                         ondelete='cascade', 
                         string="Expediente")
