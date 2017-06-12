# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class report_project_general(models.AbstractModel):
    _name = 'report.agili.report_project_general'

    def _get_data_general(self):

        #Dictionary that containt the data
        info = {}

        #Vars for the control of the data
        info['cooperative'] = False
        
        #Get all projects
        all_projects = self.env['agili.project'].search([('id', '>=', 0)])

        #Copperatives
        cooperatives = ['geekos', 
                        'bmkeros', 
                        'vultur', 
                        'tecnoparaguana', 
                        'hoatzin', 
                        '3punto0',
                        'simonrodriguez',
                        'juventudproductiva']

        bundle = []

        for cooperative in cooperatives:

            data = {}
            projects = []

            data['name'] = cooperative
            data['projects'] = 0
            data['days_plan'] = 0 
            data['days_exe'] = 0 
            data['progress'] = 0 

            total_progress = 0 

            for project in all_projects:

                for responsible in project.responsible_ids:

                    if responsible.cooperative == cooperative and not project in projects:

                        data['projects'] += 1
                        data['days_plan'] += project.days_plan
                        data['days_exe'] += project.days_exe
                        total_progress += project.pj_progress

                        #Add project to list
                        projects.append(project)

            if data['projects'] > 0:

                data['progress'] = total_progress / data['projects']
            
            bundle.append(data)

        info['cooperative'] = bundle 
    
        return info

    @api.model
    def render_html(self, docids, data=None):

        report_obj = self.env['report']
        report = report_obj._get_report_from_name('agili.report_project_general')
   
        docargs = {
            'doc_model': report.model,
            'data': self._get_data_general(),
        }

        return report_obj.render('agili.report_project_general', docargs)
    
   