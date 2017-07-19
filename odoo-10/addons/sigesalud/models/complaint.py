# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date

class Complaint(models.Model):
    
    _name = 'sigesalud.complaint'

    repayment_id = fields.Many2one('sigesalud.repayment',
                         ondelete='cascade', 
                         string="Reembolso")

    date = fields.Date(string="Fecha ", 
                        required=True,
                        default= datetime.now().date())

    description = fields.Text(string="Descripcion", 
                        required=True)

    expedient_id = fields.Many2one('sigesalud.expedient',
                         ondelete='cascade', 
                         string="Expediente")
