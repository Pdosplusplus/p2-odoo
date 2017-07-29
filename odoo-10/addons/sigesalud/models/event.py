# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Event(models.Model):

    _name = 'sigesalud.event'

    beneficiary_id = fields.Many2one('sigesalud.beneficiary',
                     ondelete='cascade',
                     string="Beneficiario")

    type_event = fields.Selection([
        ('accidente', "Accidente"),
        ('maternidad', "Maternidad"),
        ('emergencia', "Emergencia"),
        ('consulta', "Consulta"),
        ('terapia', "Terapia"),
    ], string="Tipo de evento", required=True)

    description = fields.Text(string="Descripcion", 
                       required=True)

    city = fields.Char(string="Ciudad", 
                       required=True)

    date = fields.Date(string="Fecha", 
                       required=True)

    clinic = fields.Char(string="Clinica", 
                       required=True)

    cost = fields.Char(string="Costo del evento", 
                       required=True)

    exam_ids = fields.One2many('sigesalud.exam', 
                        'event_id', 
                        string="Examenes")

    expedient_id = fields.Many2one('sigesalud.expedient',
                         ondelete='cascade', 
                         string="Expediente")

    state = fields.Selection([
        ('En Proceso', "En Proceso"),
        ('Ejecutado', "Ejecutado"),
    ], default='En Proceso')

    @api.multi
    def action_process(self):
        self.state = 'process'

    @api.multi
    def action_done(self):
        self.state = 'done'
