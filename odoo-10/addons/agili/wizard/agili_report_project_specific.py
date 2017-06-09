# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError

class AgiliProjectSpecific(models.TransientModel):
    _name = 'agili.report.project.specific'
    _description = "Reporte Especifico"

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

    responsible_id = fields.Many2one(
    	'res.users',
    	ondelete='set null', 
    	string="Cooperativista",  
    	index=True)

    days_plan = fields.Boolean(string="Dias Planificadas")
    days_exe = fields.Boolean(string="Dias Ejecutadas")
    projects = fields.Boolean(string="Proyectos")

    @api.multi
    def print_reporte(self):
        
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['cooperative',
                                'responsible_id', 
                                'days_plan', 
                                'days_exe',
                                'projects'])[0]
        
        if not data['form'].get('responsible_id') and not data['form'].get('cooperative'):
            raise UserError("Debe seleccionar una cooperativa o un responsable.")

        if not data['form'].get('days_plan') and not data['form'].get('days_exe') and not data['form'].get('projects'):
            raise UserError("Debe tildar alguno de los filtros.")
                
        return self.env['report'].get_action(self, 'agili.report_project_specific', data=data)

