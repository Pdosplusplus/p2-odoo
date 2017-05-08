# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError

class AgiliProjectSpecific(models.TransientModel):
    _name = 'agili.report.project.specific'
    _description = "Reporte Especifico de un proyecto"

    responsible_id = fields.Many2one(
    	'res.users',
    	ondelete='set null', 
    	string="Responsable",  
    	index=True)

    hour_man = fields.Boolean(string="Horas hombres Planificadas")
    hour_man_exe = fields.Boolean(string="Horas hombres Ejecutadas")

    projects = fields.Boolean(string="Proyectos")
    activities = fields.Boolean(string="Actividades")

    @api.multi
    def print_reporte(self):
        
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['responsible_id', 
                                'hour_man', 
                                'hour_man_exe',
                                'projects', 
                                'activities'])[0]
        
        if not data['form'].get('responsible_id'):
            raise UserError("Debe seleccionar un responsable.")
                
        return self.env['report'].get_action(self, 'agili.report_project_specific', data=data)

