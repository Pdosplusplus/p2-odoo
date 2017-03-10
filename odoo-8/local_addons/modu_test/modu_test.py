#!/usr/bin/env python
# -*- coding: utf-8 -*-


from openerp.osv import fields, osv

class modu_test(osv.osv):
    """docstring for modu_test"""
    _name="modu.test"

    _columns={
        'date': fields.date('date'),
        'name': fields.char('name', 
                            size=30, 
                            required=True, 
                            help="Name of the pupil"),
        'di': fields.integer('di',
                            size=10,
                            required=True,
                            help="Document Identification"),
        'note': fields.float('note',
                            size=20,
                            help="Points the pupil"),
        'active': fields.boolean('Active'),
    }

    _defaults = {
        'active': True,
    }
    