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

        info = {}

        info['responsible'] = ''
        info['days_plan'] = 0
        info['days_exe'] = 0
        info['projects'] = ''
        info['activities'] = ''
        info['advance'] = 0.0
        info['flag_days_plan'] = False
        info['flag_days_exe'] = False
        info['flag_projects'] = False
        info['flag_activities'] = False
        info['flag_advance'] = False

        responsible_id = data['form'].get('responsible_id')
        days_plan = data['form'].get('days_plan')
        days_exe = data['form'].get('days_exe')

        info['responsible'] = responsible_id[1]

        if data['form'].get('projects'):

            projects = self.env['agili.project'].search([(
                            'responsible_ids', '=', responsible_id[0])])

            info['projects'] = projects
            info['flag_projects'] = True

        if data['form'].get('activities') or days_plan or days_exe:

            activities = self.env['agili.activity'].search([(
                            'ac_responsible_id', '=', responsible_id[0])])

            days_plan = 0
            days_exe = 0

            for activity in activities:

                days_plan += activity.ac_days_plan
                days_exe += activity.ac_days_exe

            info['advance'] = days_exe * 100 / days_plan
            info['flag_advance'] = True

            if days_plan:

                info['days_plan'] = days_plan
                info['flag_days_plan'] = True

            if days_exe:

                info['days_exe'] = days_exe
                info['flag_days_exe'] = True

        return info