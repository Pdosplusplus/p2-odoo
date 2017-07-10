# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Policy(models.Model):
    
    _name = 'sigesalud.policy'

    name = fields.Char(string="Nombre", 
                        required=True)

    mount_total = fields.Float(string="Monto total contradado",
                        required=True)

    mount_coope = fields.Float(string="Monto por cooperativa",
                        required=True)

    mount_titu = fields.Float('Monto por titular',
                        required=True)

    mount_bene = fields.Float(string="Monto por beneficiario",
                        required=True)