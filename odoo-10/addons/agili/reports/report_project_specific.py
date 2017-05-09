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
        info['hour_man'] = 0
        info['hour_man_exe'] = 0
        info['projects'] = ''
        info['activities'] = ''
        info['advance'] = 0.0
        info['flag_hour_man'] = False
        info['flag_hour_man_exe'] = False
        info['flag_projects'] = False
        info['flag_activities'] = False
        info['flag_advance'] = False

        responsible_id = data['form'].get('responsible_id')
        hour_man = data['form'].get('hour_man')
        hour_man_exe = data['form'].get('hour_man_exe')

        info['responsible'] = responsible_id[1]

        if data['form'].get('projects'):

            projects = self.env['agili.project'].search([(
                            'responsible_ids', '=', responsible_id[0])])

            info['projects'] = projects
            info['flag_projects'] = True

        if data['form'].get('activities') or hour_man or hour_man_exe:

            activities = self.env['agili.activity'].search([(
                            'ac_responsible_id', '=', responsible_id[0])])

            hour_plan = 0
            hour_exe = 0

            for activity in activities:

                hour_plan += activity.ac_hour_man
                hour_exe += activity.ac_hour_man_exe

            info['advance'] = hour_exe * 100 / hour_plan
            info['flag_advance'] = True

            if hour_man:

                info['hour_man'] = hour_plan
                info['flag_hour_man'] = True

            if hour_man_exe:

                info['hour_man_exe'] = hour_exe
                info['flag_hour_man_exe'] = True

        return info