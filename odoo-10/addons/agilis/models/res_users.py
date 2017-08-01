# -*- coding: utf-8 -*-

from odoo import models, fields, api

class res_users(models.Model):
    _inherit = "res.users"

    cooperative_id = fields.Many2one('agilis.cooperative', 
                        string="Cooperativa",
                        required=True)



    