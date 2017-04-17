# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models

class report_project_general(models.AbstractModel):
    _name = 'report.agili.report_general'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('agili.report_general')
        projects = self.env['agili.project']
        docargs = {
            'doc_model': report.model,
            'docs': projects,
            'mensaje': "Prueba",
        }

        return report_obj.render('agili.report_general', docargs)
