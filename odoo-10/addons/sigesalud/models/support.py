# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Support(models.Model):
    
    _name = 'sigesalud.support'

    name = fields.Char(string="Nombre ", 
                        required=True)

    support = fields.Binary(string="Soporte", 
                              attachment=True)

    expedient_id = fields.Many2one('sigesalud.expedient',
                            ondelete='cascade', 
                            string="Expediente")