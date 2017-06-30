# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Expedient(models.Model):

    _name = 'sigesalud.expedient'

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

    name = fields.Char(string="Nombre", 
                       required=True)

    last_name = fields.Char(string="Apellido", 
                       required=True)

    birthdate = fields.Date(string="Fecha de nacimiento",
                        required=True)

    age = fields.Integer(string="Edad",
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

    type_policy = fields.Selection([
        ('1', "1"),
        ('2', "2"),
        ('3', "3"),
        ('4', "4"),
    ], string="Tipo de Poliza", required=True)

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

    disease_ids = fields.One2many('sigesalud.disease', 
                        'expedient_id', 
                        string="Enfermedades")

    beneficiary_ids = fields.One2many('sigesalud.beneficiary', 
                        'expedient_id', 
                        string="Grupo familiar / Beneficiarios")

    support_ids = fields.One2many('sigesalud.support', 
                        'support_id', 
                        string="Soportes")

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