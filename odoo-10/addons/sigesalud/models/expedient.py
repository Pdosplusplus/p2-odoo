# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from odoo.addons.sigesalud.common.utils import years


class Expedient(models.Model):

    _name = 'sigesalud.expedient'

    name = fields.Char(string="Nombre Completo", 
                       required=True)

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

    bank_account = fields.Integer(string="Numero de cuenta bancaria", 
                       required=True,
                       unique=True)

    type_account = fields.Selection([
        ('corriente', "Corriente@"),
        ('ahoroo', "Ahorro"),
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
