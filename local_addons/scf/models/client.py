# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class client (osv.osv):
    #Variable de como se va a llamar mi objeto
    #A base de este name se crea la tabla
    _name ="scf.client"

    #Aqui se define por cual atributo se hara la busqueda
    _rec_name="name"


    #Atributos de la tabla u objeto
    _columns={
        'name':         fields.char('Name', 
                            size=30, 
                            required=True, 
                            help="Name client"),
        'di':           fields.integer('Document Identification',
                            size=10,
                            required=True,
                            help="Document Identification"),
        'country_id':   fields.many2one('scf.country', 
                            'Country',
                            required=True,
                            ondelete="restrict"),
        'city_id':      fields.many2one('scf.city', 
                            'City',
                            required=True,
                            ondelete="restrict"),
        'cellphone_ids': fields.many2many('scf.cellphone', 
                            'scf_client_cellphone_rel',
                            'client_id',
                            'cellphone_id',
                            'Cell Phones',
                            ondelete="restrict"),
        'provider_ids': fields.one2many('scf.provider',
                            'client_id',
                            'Provider',
                            ondelete="restrict"),
        'active':       fields.boolean('Active',
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
