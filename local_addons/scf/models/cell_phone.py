# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class cell_phone (osv.osv):
    #Variable de como se va a llamar mi objeto
    #A base de este name se crea la tabla
    _name ="scf.cellphone"

    #Aqui se define por cual atributo se hara la busqueda
    _rec_name="number"


    #Atributos de la tabla u objeto
    _columns={
        'number':           fields.integer('Number',
                            size=10,
                            required=True,
                            help="Number of cell"),    
        'active':       fields.boolean('Active',
                            help="If he is active, include in the view"),
    }

    _defaults = {
        'active': True,
    }


