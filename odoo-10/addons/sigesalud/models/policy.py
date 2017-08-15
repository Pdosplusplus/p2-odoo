# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Policy(models.Model):
    
    _name = 'sigesalud.policy'

    name = fields.Char(string="Nombre", 
                        required=True)

    sum_assured = fields.Float(string="Suma asegurada",
                        required=True)

    range_ids = fields.Many2many('sigesalud.range', 
                        string="Rangos")

    cost = fields.Float(string="Costo",
                        compute="_cost")


    def _cost(self):

    	all_expedient = self.env['sigesalud.expedient'].search([('id', '>', 0)])

        for r in self:

            for expedient in all_expedient:

                for policy in expedient.policy_ids:

                	if policy.id == r.id:

                		for rang in policy.range_ids:
                			
            				if rang.name == 'Todas Maternidad'  or rang.name == 'Todas odontologo' or rang.name == 'Todas Muerte' or rang.name == 'Todas Funerario':

            					r.cost += rang.bounty

            				else:

            					rango = rang.name.split('-')

            					rango = range(int(rango[0]), int(rango[1]))

            					if expedient.age in rango:

            						r.cost += rang.bounty

                for beneficiary in expedient.beneficiary_ids:

                	for policy in beneficiary.policy_ids:

	                	if policy.id == r.id:

	                		for rang in policy.range_ids:

                				if rang.name == 'Todas Maternidad'  or rang.name == 'Todas odontologo' or rang.name == 'Todas Muerte' or rang.name == 'Todas Funerario':

                					r.cost += rang.bounty

                				else:

                					rango = rang.name.split('-')

                					rango = range(int(rango[0]), int(rango[1]))

                					if beneficiary.bf_age in rango:

                						r.cost += rang.bounty




