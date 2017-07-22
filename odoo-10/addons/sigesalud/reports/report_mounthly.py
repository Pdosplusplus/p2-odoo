# -*- coding: utf-8 -*-

from odoo import api, models
from odoo.addons.sigesalud.common.utils import compareMounts
from datetime import datetime, date

class ReportMounthly(models.AbstractModel):
    _name = 'report.sigesalud.report_mounthly'

    @api.model
    def render_html(self, docids, data=None):
    
        docargs = {
            'doc_model': self.env['sigesalud.expedient'],
            'data': self._get_data_specific(data),
        }

        return self.env['report'].render('sigesalud.report_mounthly', docargs)


    def _get_data_specific(self, data):

        #Dictionary that containt the data
        info = {}

        #Data send from the wizard
        month = data['form'].get('month')
        selection = data['form'].get('selection')
        cooperative = data['form'].get('cooperative')
        titular = data['form'].get('titular')
        beneficiary = data['form'].get('beneficiary')

        #Vars for the control of the data
        info['month'] = month
        info['cooperative'] = cooperative
        info['titular'] = titular
        info['beneficiary'] = beneficiary
        info['date'] = datetime.now().date() 

        cooperatives = {}
        cooperatives["name"] = cooperative
        cooperatives["beneficiaries"] = ""
        cooperatives["num_aso"] = 0
        cooperatives["events_aso"] = 0
        cooperatives["num_no_aso"] = 0
        cooperatives["events_no_aso"] = 0
        cooperatives["mount_total"] = 0
        cooperatives["mount_aso"] = 0
        cooperatives["mount_no_aso"] = 0
        cooperatives["percentage_aso"] = 0.0
        cooperatives["percentage_no_aso"] = 0.0
        cooperatives["events_total"] = 0


        #Vars to show in the report
        titulars = {}
        titulars["name"] = ""
        titulars["num_aso"] = 0
        titulars["events_aso"] = 0
        titulars["num_no_aso"] = 0
        titulars["events_no_aso"] = 0
        titulars["mount_total"] = 0
        titulars["mount_aso"] = 0
        titulars["mount_no_aso"] = 0
        titulars["percentage_aso"] = 0.0
        titulars["percentage_no_aso"] = 0.0
        titulars["events_total"] = 0

        beneficiaries = {}
        beneficiaries["name"] = ""
        beneficiaries["num"] = 0
        beneficiaries["events"] = 0
        beneficiaries["events_total"] = 0
        beneficiaries["mount"] = 0
        beneficiaries["percentage"] = 0

        if cooperative:

            if cooperative:
                #Get all expedient    
                all_expedient = self.env['sigesalud.expedient'].search([('cooperative', '=', cooperative)])

            for expedient in all_expedient:

                if expedient.associated == 'si':
                    
                    cooperatives["num_aso"] += 1
        
                else:

                    cooperatives["num_no_aso"] += 1

                cooperatives["events_total"] += len(expedient.event_ids)

                #Recorremos los eventos realizados por el titular
                for event in expedient.event_ids:

                    #Verificamos si el mes del evento es igual al seleccionado.
                    if compareMounts(month, event.date):

                        if expedient.associated == 'si':
                    
                            cooperatives["events_aso"] += 1
                            cooperatives["mount_aso"] += int(event.cost)

                        else:

                            cooperatives["events_no_aso"] += 1
                            cooperatives["mount_no_aso"] += int(event.cost)

                beneficiaries["events_total"] += len(expedient.beneficiary_ids)

                for beneficiary in expedient.beneficiary_ids:

                    for event in beneficiary.event_ids:

                        #Verificamos si el mes del evento es igual al seleccionado.
                        if compareMounts(month, event.date):

                            beneficiaries["events"] += 1
                            beneficiaries["mount"] += int(event.cost)

            if cooperatives["events_total"] > 0:

                cooperatives["percentage_aso"] = cooperatives["events_aso"] * 100 / cooperatives["events_total"]
                cooperatives["percentage_no_aso"] = cooperatives["events_no_aso"] * 100 / cooperatives["events_total"]

            cooperatives["mount_total"] = cooperatives["mount_aso"] + cooperatives["mount_no_aso"]

            if beneficiaries["events_total"] > 0:

                beneficiaries["percentage"] = beneficiaries["events"] * 100 / beneficiaries["events_total"]

            cooperatives["beneficiaries"] = beneficiaries
            info['cooperative'] = cooperatives
        
        if titular:

            all_expedient = self.env['sigesalud.expedient'].search([('id', '=', titular[0])])
            titulars["name"] = titular[1]


        if beneficiary:

            all_expedient = self.env['sigesalud.expedient'].search([('id', '>', 0)])
            
            beneficiaries["name"] = beneficiary[1]

            for expedient in all_expedient:

                for beneficiar in expedient.beneficiary_ids:

                    if beneficiar.id == beneficiary[0]:

                        beneficiaries["events_total"] = len(beneficiar.event_ids)

                        for event in beneficiar.event_ids:

                            #Verificamos si el mes del evento es igual al seleccionado.
                            if compareMounts(month, event.date):

                                beneficiaries["events"] += 1
                                beneficiaries["mount"] += int(event.cost)


            if beneficiaries["events_total"] > 0:

                beneficiaries["percentage"] = beneficiaries["events"] * 100 / beneficiaries["events_total"]

            info['beneficiary'] = beneficiaries

        return info