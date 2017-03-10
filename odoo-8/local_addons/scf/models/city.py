# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class city (osv.osv):
    #Variable de como se va a llamar mi objeto
    #A base de este name se crea la tabla
    _name ="scf.city"

    #Aqui se define por cual atributo se hara la busqueda
    _rec_name="name"


    #Atributos de la tabla u objeto
    _columns={
        'name': fields.char('Name', 
                            size=30, 
                            required=True, 
                            help="Name city"),
        'country_id':   fields.many2one('scf.country', 
                            'Country', 
                            required=True),
        'active': fields.boolean('Active',
                            help="If he is active, include in the view"),
    }

    _defaults = {
        'active': True,
    }
