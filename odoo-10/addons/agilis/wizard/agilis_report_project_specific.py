# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError

class AgilisProjectSpecific(models.TransientModel):
    _name = 'agilis.report.project.specific'
    _description = "Reporte Especifico"

    selection = fields.Selection([
        ('cooperativa', "Por Cooperativa"),
        ('cooperativista', "Por Cooperativista")
    ], string="Reporte por")

    cooperative_id = fields.Many2one('agilis.cooperative', 
                        string="Cooperativa")

    responsible_id = fields.Many2one(
    	'res.users',
    	ondelete='set null', 
    	string="Cooperativista",  
    	index=True)

    type_data= fields.Selection([
        ('project', "En un solo Proyecto"),
        ('projects', "En varios proyectos"),
        ('advances', "Todos"),
    ], string="Reporte de avances:")

    project = fields.Many2one('agilis.project', 
                        string="Proyecto")

    projects = fields.Many2many('agilis.project', 
                        string="Proyectos")


    @api.multi
    def print_reporte(self):
        
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['cooperative_id',
                                'selection',
                                'responsible_id', 
                                'type_data',
                                'project',
                                'projects'])[0]

        if not data['form'].get('selection'):
            raise UserError("Debe seleccionar el tipo de reporte que quiere")
        
        if data['form'].get('selection') == 'cooperativa' and not data['form'].get('cooperative_id'):
            raise UserError("Debe seleccionar una cooperativa.")

        if data['form'].get('selection') == 'cooperativista' and not data['form'].get('responsible_id'):
            raise UserError("Debe seleccionar a un cooperativista.")

        if data['form'].get('selection') == 'cooperativista' and not data['form'].get('type_data'):
            raise UserError("Debe seleccionar alguno de los filtros para el reporte por cooperativista.")

        if data['form'].get('selection') == 'cooperativista' and data['form'].get('type_data') == 'project' and not data['form'].get('project'):
            raise UserError("Debe seleccionar un proyecto.")

        if data['form'].get('selection') == 'cooperativista' and data['form'].get('type_data') == 'projects' and not data['form'].get('projects'):
            raise UserError("Debe seleccionar un proyecto.")
                
        return self.env['report'].get_action(self, 'agilis.report_project_specific', data=data)


    @api.onchange('selection')
    def _selection(self):

        if self.selection ==  'cooperativa':

            self.responsible_id = False
            self.projects = False
            self.deliverable = False

        if self.selection ==  'cooperativista':

            self.cooperative_id = False