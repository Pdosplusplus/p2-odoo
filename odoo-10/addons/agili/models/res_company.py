# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools
import os

class res_company(models.Model):
    _inherit = "res.company"

    def _get_logo(self):
        
        BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        return open(os.path.join(BASEDIR,
            'static',
            'src',
            'img', 
            'agili-icon-5.png'), 
            'rb') .read().encode('base64')

    logo = fields.Binary(related='partner_id.image', default=_get_logo)
