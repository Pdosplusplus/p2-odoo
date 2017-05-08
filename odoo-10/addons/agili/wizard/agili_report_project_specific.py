# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError

class AgiliProjectSpecific(models.TransientModel):
    _name = 'agili.report.project.specific'
    _description = "Reporte Especifico de un proyecto"

    project_id = fields.Many2one(
    	'agili.project',
        ondelete='cascade', 
        string="Proyecto")

    responsible_id = fields.Many2one(
    	'res.users',
    	ondelete='set null', 
    	string="Responsable",  
    	index=True)

    hour_man = fields.Integer(string="Horas hombres")

    @api.model
    def _print_report(self, data):
        
        data = self.pre_print_report(data)

        if not data['form'].get('project_id'):
            raise UserError(_("Selecciona un proyecto."))
                
        return self.env['report'].get_action('agili.report_project_general', data=data)

