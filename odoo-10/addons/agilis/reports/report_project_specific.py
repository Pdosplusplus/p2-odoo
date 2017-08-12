# -*- coding: utf-8 -*-

from odoo import api, models
from odoo.addons.agilis.common.utils import compareDates


class ReportProjectSpecific(models.AbstractModel):
    _name = 'report.agilis.report_project_specific'

    @api.model
    def render_html(self, docids, data=None):
    
        docargs = {
            'doc_model': self.env['agilis.project'],
            'data': self._get_data_specific(data),
        }

        return self.env['report'].render('agilis.report_project_specific', docargs)


    def _get_data_specific(self, data):

        #Dictionary that containt the data
        info = {}

        #Data send from the wizard
        cooperative = data['form'].get('cooperative_id')
        responsible_id = data['form'].get('responsible_id')
        type_data = data['form'].get('type_data')
        selection = data['form'].get('selection')
        pj = data['form'].get('project')

        #Vars for the control of the data
        info['cooperative'] = False
        info['responsible'] = False
        info['projects'] = []

        print(str(cooperative))

        #Get all projects
        all_projects = self.env['agilis.project'].search([('id', '>', 0)])

        if cooperative:

            info['cooperative'] = cooperative[1]

            for proyecto in all_projects:

                for coope in proyecto.cooperative_ids:

                    if coope.id == cooperative[0]:

                        project = {}
                        project["name"] = proyecto.name
                        project["start_date"] = '2017-12-31' 
                        project["end_date"] = '2017-01-01'
                        project["journal_plan"] = 0
                        project["journal_exe"] = 0
                        project["progress"] = 0

                        for tri in proyecto.trimestre_ids:

                            if compareDates(tri.date_ini, project["start_date"], 'less'):

                                project["start_date"] = tri.date_ini

                            if compareDates(tri.date_end, project["start_date"], 'higher'):

                                project["end_date"] = tri.date_end

                        for activity in proyecto.activity_ids:

                            for cooperativista in activity.cooperativista_ids:

                                if cooperativista.cooperative_id.id == cooperative[0]:

                                    project["journal_plan"] += activity.journals_plan
                                    project["journal_exe"] += activity.journals_exe

                        for load in proyecto.load_ids:

                            if load.cooperative_id.id == cooperative[0]:

                                project["journal_plan"] += load.journals


                        if project["journal_plan"] > 0 and project["journal_exe"] > 0:

                            project["progress"] = project["journal_exe"] * 100 / project["journal_plan"]

                        info['projects'].append(project)

        if responsible_id:

            info['responsible'] = responsible_id[1]

            all_bitacora = self.env['agilis.bitacora'].search([('write_uid.id', '=', responsible_id[0])])

            if type_data == 'project':

                for proyecto in all_projects:

                    if proyecto.id == pj[0]:

                        project = {}
                        project["name"] = proyecto.name
                        project["start_date"] = '2017-12-31' 
                        project["end_date"] = '2017-01-01'
                        project["journal_plan"] = 0
                        project["journal_exe"] = 0
                        project["progress"] = 0
                        project["bitacoras"] = []

                        for tri in proyecto.trimestre_ids:

                            if compareDates(tri.date_ini, project["start_date"], 'less'):

                                project["start_date"] = tri.date_ini

                            if compareDates(tri.date_end, project["start_date"], 'higher'):

                                project["end_date"] = tri.date_end

                        for bita in all_bitacora:

                            if bita.activity_id.project_id.id == proyecto.id:

                                bitacora = {}
                                bitacora["activity"] = bita.activity_id.name
                                bitacora["date"] = bita.date
                                bitacora["description"] = bita.description
                                bitacora["journals"] = bita.journals

                                project["bitacoras"].append(bitacora)

                    info['projects'].append(project)

        print(str(info['projects'][0]['name']))
        
        return info