# -*- coding: utf-8 -*-

from odoo import api, models
from odoo.addons.sigesalud.common.utils import compareMounts, diff_days

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
        selection_event = data['form'].get('selection_event')

        #Vars for the control of the data
        info['month'] = month
        info['cooperative'] = cooperative
        info['titular'] = titulars
        info['beneficiary'] = beneficiary
        info['date'] = datetime.now().date() 
        info['event'] = type_event
        info['repayment'] = repayment
        info['use_days'] = diff_days()
        info['all_titu'] = []
        info['all_bene'] = []
        info['all_coope'] = []
        info['selection_event'] = selection_event
        info['events'] = []
        
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

        if selection == 'all_titu':

            all_expedient = self.env['sigesalud.expedient'].search([('id', '>', 0)])

            for expedient in all_expedient:

                titular = {}
                titular["name"] = ""
                titular["cooperative"] = 0
                titular["num_events"] = 0
                titular["type_events"] = 0
                titular["total_events"] = 0
                titular["mount"] = 0
                titular["porcentage_use"] = 0

                events = []

                titular["name"] = expedient.name
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

                info['all_titu'].append(titular)

        if selection == 'all_bene':

            all_expedient = self.env['sigesalud.expedient'].search([('id', '>', 0)])

            for expedient in all_expedient:

                for beneficiary in expedient.beneficiary_ids:

                    beneficiaries = {}
                    beneficiaries["name"] = ""
                    beneficiaries["cooperative"] = ""
                    beneficiaries["relationship"] = ""
                    beneficiaries["num_events"] = 0
                    beneficiaries["type_events"] = 0
                    beneficiaries["total_events"] = 0
                    beneficiaries["mount"] = 0
                    beneficiaries["porcentage_use"] = 0

                    events = []

                    beneficiaries["name"] = beneficiary.name
                    beneficiaries["cooperative"] = expedient.cooperative
                    beneficiaries["relationship"] = beneficiary.relationship

                    for event in expedient.event_ids:

                        if event.beneficiary_id.id == beneficiary.id:

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

                    info['all_bene'].append(beneficiaries)


        if selection == 'all_coope':

            cooperativas = ['Geekos', 'Bmkeros', 'Vultur', 'Tecno Paraguana', 'Sinapsis']
  
            for coope in cooperativas:

                #Get all expedient    
                all_expedient = self.env['sigesalud.expedient'].search([('cooperative', '=', coope)])

                cooperatives = {}
                cooperatives["name"] = coope
                cooperatives["num_titu"] = 0
                cooperatives["num_beneficiaries"] = 0
                cooperatives["num_events"] = 0
                cooperatives["type_events"] = 0
                cooperatives["total_events"] = 0
                cooperatives["mount"] = 0
                cooperatives["porcentage_use"] = 0 

                events = []

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

                info['all_coope'].append(cooperatives)


        if selection_event == 'todos':
            
            event_hospi = {}
            event_hospi['name'] = 'Hospitalizacion'
            event_hospi['num'] = 0
            event_hospi['cost'] = 0
            event_hospi['frequ'] = 0

            event_mater = {}
            event_mater['name'] = 'Maternidad'
            event_mater['num'] = 0
            event_mater['cost'] = 0
            event_mater['frequ'] = 0

            event_emer = {}
            event_emer['name'] = 'Emergencia'
            event_emer['num'] = 0
            event_emer['cost'] = 0
            event_emer['frequ'] = 0

            event_consul = {}
            event_consul['name'] = 'Consulta'
            event_consul['num'] = 0
            event_consul['cost'] = 0
            event_consul['frequ'] = 0

            event_tera = {}
            event_tera['name'] = 'Terapia'
            event_tera['num'] = 0
            event_tera['cost'] = 0
            event_tera['frequ'] = 0

            event_ciru = {}
            event_ciru['name'] = 'Cirugia'
            event_ciru['num'] = 0
            event_ciru['cost'] = 0
            event_ciru['frequ'] = 0

            all_expedient = self.env['sigesalud.expedient'].search([('id', '>', 0)])

            for expedient in all_expedient:

                all_events = len(expedient.event_ids)

                for event in expedient.event_ids:

                    #Verificamos si el mes del evento es igual al seleccionado.
                    if compareMounts(month, event.date):

                        if event.type == 'hospitalizacion':

                            event_hospi['num'] += 1
                            event_hospi['cost'] += event.cost 
                            event_hospi['frequ'] = event_hospi['num'] * 100 / all_events 

                        if event.type == 'maternidad':

                            event_mater['num'] += 1
                            event_mater['cost'] += event.cost 
                            event_mater['frequ'] = event_mater['num'] * 100 / all_events

                        if event.type == 'emergencia':

                            event_emer['num'] += 1
                            event_emer['cost'] += event.cost
                            event_emer['frequ'] = event_emer['num'] * 100 / all_events

                        if event.type == 'consulta':

                            event_consul['num'] += 1
                            event_consul['cost'] += event.cost 
                            event_consul['frequ'] = event_consul['num'] * 100 / all_events

                        if event.type == 'terapia':

                            event_tera['num'] += 1
                            event_tera['cost'] += event.cost 
                            event_tera['frequ'] = event_tera['num'] * 100 / all_events

                        if event.type == 'cirugia':

                            event_ciru['num'] += 1
                            event_ciru['cost'] += event.cost
                            event_ciru['frequ'] = event_ciru['num'] * 100 / all_events


            info['events'].append(event_hospi)
            info['events'].append(event_mater)
            info['events'].append(event_emer)
            info['events'].append(event_consul)
            info['events'].append(event_hospi)
            info['events'].append(event_tera)
            info['events'].append(event_ciru)
                
        return info