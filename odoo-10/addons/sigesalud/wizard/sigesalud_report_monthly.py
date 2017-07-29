# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError

class SigesaludReportMounthly(models.TransientModel):
    _name = 'sigesalud.report.mounthly'
    _description = "Reporte Mensual"

    month = fields.Selection([
        ('1', "Enero"),
        ('2', "Febrero"),
        ('3', "Marzo"),
        ('4', "Abril"),
        ('5', "Mayo"),
        ('6', "Junio"),
        ('7', "Julio"),
        ('8', "Agosto"),
        ('9', "Septiembre"),
        ('10', "Octubre"),
        ('11', "Noviembre"),
        ('12', "Diciembre"),
    ], string="Mes")

    selection = fields.Selection([
        ('cooperativa', "Cooperativa"),
        ('titular', "Titular"),
        ('beneficiario', "Beneficiario"),
        ('evento', "Evento"),
        ('reembolso', "Reembolso"),
    ], string="Reporte por")

    cooperative = fields.Selection([
        ('geekos', "Geekos"),
        ('bmkeros', "Bmkeros"),
        ('vultur', "Vultur"),
        ('tecnoparaguana', "Tecno Paraguana"),
        ('hoatzin', "Hoatzin"),
        ('3punto0', "Tres Punto Cero"),
        ('simonrodriguez', "Simon Rodriguez"),
        ('juventudproductiva', "Juventud Productiva"),
    ], string="Cooperativa")

    titular = fields.Many2one(
    	'sigesalud.expedient',
    	ondelete='set null', 
    	string="Titular",  
    	index=True)

    beneficiary = fields.Many2one(
        'sigesalud.beneficiary',
        ondelete='set null', 
        string="Beneficiario",  
        index=True)

    type_event = fields.Selection([
        ('accidente', "Accidente"),
        ('maternidad', "Maternidad"),
        ('emergencia', "Emergencia"),
        ('consulta', "Consulta"),
        ('terapia', "Terapia"),
        ('medicina', "Medicina"),
    ], string="Tipo de evento")

    type_repayment = fields.Selection([
        ('process', "En proceso"),
        ('maternidad', "Ejecutado"),
        ('cancel', "Cancelado"),
    ], string="Tipo de evento")

    @api.multi
    def print_reporte(self):
        
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['month',
                                'selection',
                                'cooperative', 
                                'titular', 
                                'beneficiary',
                                'type_event',
                                'type_repayment'])[0]
        
        if not data['form'].get('month'):
            raise UserError("Debe seleccionar un mes")

        if not data['form'].get('selection'):
            raise UserError("Debe seleccionar el tipo de reporte que quiere")

        if data['form'].get('selection') == 'cooperativa' and not data['form'].get('cooperative'):
            raise UserError("Debe seleccionar una cooperativa.")

        if data['form'].get('selection') == 'titular' and not data['form'].get('titular'):
            raise UserError("Debe seleccionar un titular.")

        if data['form'].get('selection') == 'beneficiario' and not data['form'].get('beneficiary'):
            raise UserError("Debe seleccionar un beneficiario.")

        if data['form'].get('selection') == 'evento' and not data['form'].get('type_event'):
            raise UserError("Debe seleccionar el tipo de evento.")

        if data['form'].get('selection') == 'reembolso' and not data['form'].get('type_repayment'):
            raise UserError("Debe seleccionar el tipo de reembolso.")
                
        return self.env['report'].get_action(self, 'sigesalud.report_mounthly', data=data)

