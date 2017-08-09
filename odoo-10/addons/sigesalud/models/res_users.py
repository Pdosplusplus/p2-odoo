# -*- coding: utf-8 -*-

from odoo import models, fields, api

class res_users(models.Model):
    _inherit = "res.users"

    cooperative = fields.Selection([
        ('Geekos', "Geekos"),
        ('Bmkeros', "Bmkeros"),
        ('Vultur', "Vultur"),
        ('Tecno Paraguana', "Tecno Paraguana"),
        ('Sinapsis', "Sinapsis"),
    ], string="Cooperativa")

