# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Document(models.Model):
    
    _name = 'sigesalud.document'

    type_doc = fields.Selection([
        ('im', "Informe Medico"),
        ('rt', "Recipe de Tratamiento"),
        ('it', "Indicaciones de Tratamiento"),
        ('oem', "Ordenes de examenes medicos"),
        ('rem', "Resultado de examenes medicos"),
        ('fcm', "Factura consulta medica"),
        ('fem', "Factura de examenes medicos"),
        ('fmt', "Factura de medicinas por tratamiento"),
        ('imt', "Informe medico de terapias"),
        ('gt', "Gastos en terapias"),
    ], string="Tipo de documento")

    original = fields.Boolean(string="Original ", 
                        required=True)

    copy = fields.Boolean(string="Copia",
                        required=True)

    date = fields.Date(string="Fecha",
                        required=True)

    cost = fields.Float(string="Costo",
                        required=True)

    support = fields.Binary(string="Soporte digital", 
                        attachment=True,
                        required=True)

    repayment_id = fields.Many2one('sigesalud.repayment',
                     ondelete='cascade',
                     string="Reembolso")
