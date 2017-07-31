# -*- coding: utf-8 -*-

from odoo import models, fields, api

class res_users(models.Model):
    _inherit = "res.users"

    cooperative = fields.Selection([
        ('Geekos', "Geekos"),
        ('Bmkeros', "Bmkeros"),
        ('Vultur', "Vultur"),
        ('Tecno Paraguana', "Tecno Paraguana"),
        ('Hoatzin', "Hoatzin"),
        ('Tres Punto Cero', "Tres Punto Cero"),
        ('Simon Rodriguez', "Simon Rodriguez"),
        ('Juventud Productiva', "Juventud Productiva"),
        ('Sinapsis', "Sinapsis"),
    ], string="Cooperativa")

