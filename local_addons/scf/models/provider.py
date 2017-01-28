# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class provider (osv.osv):
    #Variable de como se va a llamar mi objeto
    #A base de este name se crea la tabla
    _name ="scf.provider"

    #Aqui se define por cual atributo se hara la busqueda
    _rec_name="name"


    #Atributos de la tabla u objeto
    _columns={
        'name':         fields.char('Name', 
                            size=30, 
                            required=True, 
                            help="Name provider"),
        'di':           fields.integer('Document Identification',
                            size=10,
                            required=True,
                            help="Document Identification"),
        'country_id':   fields.many2one('scf.country', 
                            'Country',
                            required=True),
        'city_id':      fields.many2one('scf.city', 
                            'City',
                            required=True),
        'client_id':    fields.many2one('scf.client',
                            'Client'),
        'active': fields.boolean('Active',
                            help="If he is active, include in the view"),
    }

    _defaults = {
        'active': True,
    }

    def clean_city(self, cr, ids, context=None):

        return {
                'value': {
                            'city_id': ''
                          }
               }