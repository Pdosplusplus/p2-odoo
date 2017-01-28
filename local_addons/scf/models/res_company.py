# -*- coding: utf-8 -*-
import inspect, os
from openerp.osv import fields, osv

class res_company (osv.osv):
    #Variable de como se va a llamar mi objeto
    #A base de este name se crea la tabla
    _name="res.company"

    #Aqui le decimos de donde hereda esta clase
    _inherit=['res.company']

    # Heredamos el metodo y lo sobreescribrimos
    # Este metodo corresponde el logo


    def _get_logo(self, cr, uid, ids):

        ruta_actual=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe)))
        ruta_actual=ruta_actual.split('models')
        ruta_actual=''.join(ruta_actual)

        return open(os.path.join(
                        ruta_actual,
                        'static',
                        'img',
                        'geek.jpeg'
                        )           
                    ,'rb').read().encode('base64')

    #Atributos de la tabla u objeto
    _columns={
        'rif': fields.char('RIF', 
                            size=10, 
                            required=True, 
                            help="RIF"),
    }

    _defaults={
        'logo':_get_logo,
    }
    