# -*- coding: utf-8 -*-

from odoo import api, models

class ReportProjectSpecific(models.AbstractModel):
    _name = 'report.agili.report_project_specific'

    @api.model
    def render_html(self, docids, data=None):

        projects = self.env['agili.project'].search([('id','==', data['form'].get('project_id'))])
        
        docargs = {
            'doc_model': report.model,
            'data': projects,
        }

        return report_obj.render('agili.report_project_specific', docargs)