# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Activity(models.Model):

    _name = 'dailyac.activity'

    day = fields.Date(string="Día", required=True)

    name = fields.Char(string="Nombre de Actividad", required=True)

    objetive = fields.Char(string="Objetivo", required=True)
    
    description = fields.Text(string="Descripción")

    result = fields.Text(string="Resultado")

    who_summon = fields.Many2one('res.partner',
    ondelete='set null', string="Quién generó la convocatoria ?", index=True)

    responsible_id = fields.Many2one('res.users',
    ondelete='set null', string="Responsable", index=True)

    
class Session(models.Model):

    _name = 'dailyac.session'

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")

    instructor_id = fields.Many2one('res.partner', string="Instructor")
    activity_id = fields.Many2one('dailyac.activity',
        ondelete='cascade', string="Actividad", required=True)

