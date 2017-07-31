# -*- coding: utf-8 -*-

from odoo import models, fields, api

class res_users(models.Model):
    _inherit = "res.users"

    cooperative = fields.Selection([
        ('geekos', "Geekos"),
        ('bmkeros', "Bmkeros"),
        ('vultur', "Vultur"),
        ('tecnoparaguana', "Tecno Paraguana"),
        ('hoatzin', "Hoatzin"),
        ('3punto0', "Tres Punto Cero"),
        ('simonrodriguez', "Simon Rodriguez"),
        ('juventudproductiva', "Juventud Productiva"),
    ], string="Cooperativa")




    