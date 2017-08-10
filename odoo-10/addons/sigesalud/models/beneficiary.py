# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.addons.sigesalud.common.utils import years

class Beneficiart(models.Model):

    _name = 'sigesalud.beneficiary'

    relationship = fields.Selection([
        ('padre', "Padre"),
        ('madre', "Madre"),
        ('conyuge', "Conyuge"),
        ('hijo', "Hijo"),
        ('hermano', "Hermano"),

    ], string="Parentesco", required=True)

    name = fields.Char(string="Nombre Completo", 
                       required=True)

    bf_birthdate = fields.Date(string="Fecha de nacimiento",
                        required=True)

    bf_age = fields.Integer(string="Edad",
                        compute="_years",
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

    bf_ci = fields.Char(string="Cedula de identidad",
                        unique=True,
                        size=9)

    bf_celphone = fields.Char(string="Numero telefonico", 
                        size=11,
                       required=True)

    bf_email = fields.Char(string="Correo Electronico",
                       unique=True)

    bf_address = fields.Text(string="Direccion", 
                       required=True)

    expedient_id = fields.Many2one('sigesalud.expedient',
                            ondelete='cascade', 
                            string="Expediente")

    policy_ids = fields.Many2many('sigesalud.policy', string="Polizas")
    
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

    @api.onchange('bf_birthdate')
    def _years(self):

        for r in self:
            
            if r.bf_birthdate:
                
                if years(r.bf_birthdate) < 0:

                    raise ValidationError('La fecha de nacimiento es erronea, por favor seleccione una fecha valida')

                r.bf_age = years(r.bf_birthdate)


    @api.constrains('bf_celphone')
    def _check_celphone(self):

        bf_celphone = self.bf_celphone
        
        if bf_celphone and len(bf_celphone) < 11:
        
            raise ValidationError('El numero de telefono debe contener 11 digitos, por favor ingrese un numero valido')

        try:
            return int(bf_celphone)

        except ValueError:
        
            raise ValidationError('Por favor el campo telefono solo permite numeros.')


    @api.constrains('bf_ci')
    def _check_ci(self):

        for r in self:

            if r.bf_age >= 9:

                if r.bf_ci == '':

                    raise ValidationError('El campo cedula es requerido')

                try:
                    return int(r.bf_ci)

                except ValueError:
                
                    raise ValidationError('Por favor el campo cedula solo permite numeros.')