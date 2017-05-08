# -*- coding: utf-8 -*-

from odoo import api, models

class ReportProjectSpecific(models.AbstractModel):
    _name = 'report.agili.report_project_specific'

    @api.model
    def render_html(self, docids, data=None):
    
        docargs = {
            'doc_model': self.env['agili.project'],
            'data': _get_data_specific(self, data),
        }

        return self.env['report'].render('agili.report_project_specific', docargs)


    def _get_data_specific(self, data):

        info = {}

        responsible_id = data['form'].get('responsible_id')

        projects = self.env['agili.project'].search([(
                            'responsible_id', '=', responsible_id[0])])

        activities = self.env['agili.activity'].search([(
                            'ac_responsible_id', '=', responsible_id[0])])


        return projects