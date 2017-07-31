# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from odoo.addons.sigesalud.common.utils import years, sendEmail, FORMA_DATE
from odoo.exceptions import ValidationError

class Expedient(models.Model):

    _name = 'sigesalud.expedient'

    name = fields.Char(string="Nombre Completo", 
                       required=True)

    cooperative = fields.Selection([
        ('Geekos', "Geekos"),
        ('Bmkeros', "Bmkeros"),
        ('Vultur', "Vultur"),
        ('Tecno Paraguana', "Tecno Paraguana"),
        ('Hoatzin', "Hoatzin"),
        ('Tres Punto Cero', "Tres Punto Cero"),
        ('Simon Rodriguez', "Simon Rodriguez"),
        ('Juventud Productiva', "Juventud Productiva"),
        ('Sinapsis', "Sinapsis"),
    ], string="Cooperativa")

    associated = fields.Selection([
        ('si', "Si"),
        ('no', "No"),
    ], string="Asociado")

    birthdate = fields.Date(string="Fecha de nacimiento",
                        required=True)

    age = fields.Integer(string="Edad",
                        compute="_years",
                        required=True)

    sex = fields.Selection([
        ('masculino', "Masculino"),
        ('femenino', "Femenino"),
    ], string="Sexo", required=True)

    civil_status = fields.Selection([
        ('solter@', "Solter@"),
        ('casad@', "Casad@"),
        ('divorciad@', "Divorciad@"),
        ('viud@', "Viud@"),
    ], string="Estado Civil", required=True)

    ci = fields.Integer(string="Cedula de identidad",
                        required=True,
                        unique=True)

    celphone = fields.Char(string="Numero telefonico", 
                       required=True)

    email = fields.Char(string="Correo Electronico", 
                       required=True,
                       unique=True)

    address = fields.Text(string="Direccion", 
                       required=True)

    bank = fields.Selection([
        ('venezuela', "Venezuela"),
        ('banesco', "Banesco"),
        ('provincial', "Provincial"),
        ('tesoro', "Tesoro"),
    ], string="Banco", required=True)

    bank_account = fields.Char(string="Numero de cuenta bancaria",
                        size=20, 
                        required=True,
                        unique=True)

    type_account = fields.Selection([
        ('Corriente', "Corriente"),
        ('Ahorro', "Ahorro"),
    ], string="Tipo de cuenta", required=True)

    policy_ids = fields.Many2many('sigesalud.policy', string="Polizas")

    disease_ids = fields.One2many('sigesalud.disease', 
                        'expedient_id', 
                        string="Enfermedades")

    beneficiary_ids = fields.One2many('sigesalud.beneficiary', 
                        'expedient_id', 
                        string="Grupo familiar / Beneficiarios")

    support_ids = fields.One2many('sigesalud.support', 
                        'expedient_id', 
                        string="Soportes")

    event_ids = fields.One2many('sigesalud.event', 
                        'expedient_id', 
                        string="Soportes")

    repayment_ids = fields.One2many('sigesalud.repayment', 
                        'expedient_id', 
                        string="Reembolsos")

    complaint_ids = fields.One2many('sigesalud.complaint', 
                        'expedient_id', 
                        string="Reclamos")

    _sql_constraints = [
        ('ci_unique',
        'UNIQUE(ci)',
        "La cedula digitada ya se encuentra registrada"),

        ('email_unique',
        'UNIQUE(email)',
        "El correo digitado ya se encuentra registrado"),

        ('bank_account_unique',
        'UNIQUE(bank_account)',
        "El numero de cuenta digitado ya se encuentra registado"),

    ]

    @api.depends('birthdate')
    def _years(self):

        for r in self:
            
            r.age = years(r.birthdate)


    @api.constrains('bank_account')
    def _check_number(self):

        bank_account = self.bank_account
        
        if bank_account and len(bank_account) < 20:
        
            raise ValidationError('El numero de cuenta debe contener 20 digitos, por favor ingrese un numero de cuenta valido')

        try:
            return int(bank_account)

        except ValueError:
        
            raise ValidationError('Por favor digite solo numeros.')


    @api.multi
    def send_alert(self):

        expedients = self.env['sigesalud.expedient'].search([('id','>=', 0)])

        for expedient in expedients:

            for repayment in expedient.repayment_ids:

                ini_date = datetime.strptime(repayment.date, FORMA_DATE)
                end_date = datetime.strptime(datetime.now(), FORMA_DATE)
            
                days = str((end_date-ini_date).days)

                if days >= 40 and repayment.state == 'En Proceso':

                    info = {}
                    info['name'] = expedient.name
                    info['date'] = end_date
                    info['id'] = repayment.id

                    addressee = "vpino.geekos@test.com"
                
                    response = sendEmail(addressee, info, emitter=None)
