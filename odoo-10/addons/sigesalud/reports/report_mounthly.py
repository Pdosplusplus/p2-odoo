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
        titulars = data['form'].get('titular')
        beneficiary = data['form'].get('beneficiary')
        type_event = data['form'].get('type_event')
        repayment = data['form'].get('type_repayment')

        #Vars for the control of the data
        info['month'] = month
        info['cooperative'] = cooperative
        info['titular'] = titulars
        info['beneficiary'] = beneficiary
        info['date'] = datetime.now().date() 
        info['event'] = type_event
        info['repayment'] = repayment

        cooperatives = {}
        cooperatives["name"] = cooperative
        cooperatives["num_titu"] = 0
        cooperatives["num_beneficiaries"] = 0
        cooperatives["num_events"] = 0
        cooperatives["type_events"] = 0
        cooperatives["total_events"] = 0
        cooperatives["mount"] = 0
        cooperatives["porcentage_use"] = 0 

        #Vars to show in the report
        titular = {}
        titular["name"] = ""
        titular["cooperative"] = 0
        titular["num_events"] = 0
        titular["type_events"] = 0
        titular["total_events"] = 0
        titular["mount"] = 0
        titular["porcentage_use"] = 0

        beneficiaries = {}
        beneficiaries["name"] = ""
        beneficiaries["cooperative"] = ""
        beneficiaries["relationship"] = ""
        beneficiaries["num_events"] = 0
        beneficiaries["type_events"] = 0
        beneficiaries["total_events"] = 0
        beneficiaries["mount"] = 0
        beneficiaries["porcentage_use"] = 0

        evento = {}
        evento["name"] = type_event
        evento["num"] = 0
        evento["mount"] = 0

        repayments = {}
        repayments["name"] = repayment
        repayments["num"] = 0
        repayments["num_total"] = 0
        repayments["porcentage_use"] = 0

        events = []

        if cooperative:

            #Get all expedient    
            all_expedient = self.env['sigesalud.expedient'].search([('cooperative', '=', cooperative)])

            cooperatives["num_titu"] = len(all_expedient)

            for expedient in all_expedient:

                cooperatives["total_events"] += len(expedient.event_ids)

                #Recorremos los eventos realizados por el titular
                for event in expedient.event_ids:

                    #Verificamos si el mes del evento es igual al seleccionado.
                    if compareMounts(month, event.date):

                        cooperatives["num_events"] += 1
                        cooperatives["mount"] += float(event.cost)

                        if not event.type_event in events:

                            events.append(event.type_event)

                    cooperatives["num_beneficiaries"] = len(expedient.beneficiary_ids)

            if cooperatives["total_events"] > 0:

                cooperatives["porcentage_use"] = cooperatives["num_events"] * 100 / cooperatives["total_events"]

            cooperatives["type_events"] = events
            info['cooperative'] = cooperatives
        
        if titulars:

            expedient = self.env['sigesalud.expedient'].search([('id', '=', titulars[0])])
            
            titular["name"] = titulars[1]
            titular["cooperative"] = expedient.cooperative
            titular["total_events"] = len(expedient.event_ids)

            for event in expedient.event_ids:

                if event.beneficiary_id != True:

                    #Verificamos si el mes del evento es igual al seleccionado.
                    if compareMounts(month, event.date):

                        titular["num_events"] += 1
                        titular["mount"] += float(event.cost)

                        if not event.type_event in events:

                            events.append(event.type_event)

            if titular["total_events"] > 0:

                titular["porcentage_use"] = titular["num_events"] * 100 / titular["total_events"]

            titular["type_events"] = events
            info['titular'] = titular

        if beneficiary:

            all_expedient = self.env['sigesalud.expedient'].search([('id', '>', 0)])
            
            beneficiaries["name"] = beneficiary[1]

            for expedient in all_expedient:

                for event in expedient.event_ids:

                    if event.beneficiary_id.id == beneficiary[0]:

                        beneficiaries["cooperative"] = expedient.cooperative
                        beneficiaries["relationship"] = event.beneficiary_id.relationship
                        beneficiaries["total_events"] += 1

                        #Verificamos si el mes del evento es igual al seleccionado.
                        if compareMounts(month, event.date):

                            beneficiaries["num_events"] += 1
                            beneficiaries["mount"] += float(event.cost)

                            if not event.type_event in events:

                                events.append(event.type_event)


            if beneficiaries["total_events"] > 0:

                beneficiaries["porcentage_use"] = beneficiaries["num_events"] * 100 / beneficiaries["total_events"]

            beneficiaries["type_events"] = events
            info['beneficiary'] = beneficiaries

        if type_event:

            all_expedient = self.env['sigesalud.expedient'].search([('id', '>', 0)])
            
            for expedient in all_expedient:

                for event in expedient.event_ids:

                    if event.type_event == type_event:

                        #Verificamos si el mes del evento es igual al seleccionado.
                        if compareMounts(month, event.date):

                            evento["num"] += 1
                            evento["mount"] += float(event.cost)

            info['event'] = evento

        if repayment:

            all_expedient = self.env['sigesalud.expedient'].search([('id', '>', 0)])
            
            for expedient in all_expedient:

                repayments["num_total"] += len(expedient.repayment_ids)

                for repay in expedient.repayment_ids:

                    if repay.state == repayment:

                        repayments["num"] += 1

            if repayments["num_total"] > 0:

                repayments['porcentage_use'] = repayments["num"] * 100 / repayments["num_total"]

            info['repayment'] = repayments

        return info