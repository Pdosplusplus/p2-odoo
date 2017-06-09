# -*- coding: utf-8 -*-

from odoo import api, models

class ReportProjectSpecific(models.AbstractModel):
    _name = 'report.agili.report_project_specific'

    @api.model
    def render_html(self, docids, data=None):
    
        docargs = {
            'doc_model': self.env['agili.project'],
            'data': self._get_data_specific(data),
        }

        return self.env['report'].render('agili.report_project_specific', docargs)


    def _get_data_specific(self, data):

        #Dictionary that containt the data
        info = {}

        #Data send from the wizard
        cooperative = data['form'].get('cooperative')
        responsible_id = data['form'].get('responsible_id')
        projects_flag = data['form'].get('projects')
        days_plan_flag = data['form'].get('days_plan')
        days_exe_flag = data['form'].get('days_exe')

        #Vars for the control of the data
        info['cooperative'] = False
        info['responsible'] = False
        info['projects'] = False
        info['days_plan'] = 0
        info['days_exe'] = 0
    
        if cooperative:

            info['cooperative'] = cooperative

            if projects_flag:

                projects = []

                all_projects = self.env['agili.project'].search([('days_plan', '>=', 0)])

                for project in all_projects:

                    total_dp = 0
                    total_dexe = 0

                    if days_plan_flag or days_exe_flag:

                        total_dp += project.days_plan
                        total_dexe += project.days_exe

                    for responsible in project.responsible_ids:

                        if responsible.cooperative == cooperative and not project in projects:

                            #Add project to list
                            projects.append(project)

                #Save the list of projects
                info['projects'] = projects
                info['flag_projects'] = True

                #Save the days with either the user or the cooperative 
                info['days_plan'] = total_dp
                info['days_exe'] = total_dexe

        return info