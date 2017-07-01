# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Beneficiart(models.Model):

    _name = 'sigesalud.beneficiary'

    relationship = fields.Selection([
        ('padre', "Padre"),
        ('madre', "Madre"),
        ('conyuge', "Conyuge"),
        ('hijo', "Hijo"),
        ('hermano', "Hermano"),

    ], string="Estado Civil", required=True)

    bf_name = fields.Char(string="Nombre Completo", 
                       required=True)

    bf_birthdate = fields.Date(string="Fecha de nacimiento",
                        required=True)

    bf_age = fields.Integer(string="Edad",
                        required=True)

    bf_sex = fields.Selection([
        ('masculino', "Masculino"),
        ('femenino', "Femenino"),
    ], string="Sexo", required=True)

    bf_civil_status = fields.Selection([
        ('solter@', "Solter@"),
        ('casad@', "Casad@"),
        ('divorciad@', "Divorciad@"),
        ('viud@', "Viud@"),
    ], string="Estado Civil", required=True)

    bf_ci = fields.Integer(string="Cedula de identidad",
                        required=True,
                        unique=True)

    bf_celphone = fields.Char(string="Numero telefonico", 
                       required=True)

    bf_email = fields.Char(string="Correo Electronico", 
                       required=True,
                       unique=True)

    bf_address = fields.Char(string="Direccion", 
                       required=True)

    expedient_id = fields.Many2one('sigesalud.expedient',
                            ondelete='cascade', 
                            string="Expediente")
    
    bf_disease_ids = fields.One2many('sigesalud.disease', 
                        'beneficiary_id', 
                        string="Enfermedades")

    _sql_constraints = [
        ('bf_ci_unique',
        'UNIQUE(bf_ci)',
        "La cedula digitada ya se encuentra registrada"),

        ('bf_email_unique',
        'UNIQUE(bf_email)',
        "El correo digitado ya se encuentra registrado"),

    ]