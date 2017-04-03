# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api, exceptions

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

    session_ids = fields.One2many(
        'dailyac.session', 'activity_id', string="Sessions")

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
        [('name', '=like', u"Copy of {}%".format(self.name))])
        
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)


    _sql_constraints = [
        ('name_description_check',
        'CHECK(name != description)',
        "The title of the course should not be the description"),

        ('name_unique',
        'UNIQUE(name)',
        "The course title must be unique"),
    ]



    
class Session(models.Model):

    _name = 'dailyac.session'

    name = fields.Char(required=True)

    start_date = fields.Date(default=fields.Date.today)

    duration = fields.Float(digits=(6, 2), help="Duration in days")

    seats = fields.Integer(string="Number of seats")

    active = fields.Boolean(default=True)

    instructor_id = fields.Many2one('res.partner', string="Instructor",
            domain=['|', ('instructor', '=', True),
                 ('category_id.name', 'ilike', "Teacher")])


    activity_id = fields.Many2one('dailyac.activity',
        ondelete='cascade', string="Actividad", required=True)
    
    attendee_ids = fields.Many2many('res.partner', string="Asistentes")

    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')

    """
    Tip

    the inverse function makes the field writable, and allows 
    moving the sessions (via drag and drop) in the calendar 
    view
    """
    end_date = fields.Date(string="End Date", store=True,
        compute='_get_end_date', inverse='_set_end_date')

    hours = fields.Float(string="Duration in hours",
        compute='_get_hours', inverse='_set_hours')

    attendees_count = fields.Integer(string="Attendees count", 
        compute='_get_attendees_count', store=True)


    #Computed Field
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats


    #When change a value in the interface of client, in this case seats
    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
                return {
                    'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative",
                    },
                }

        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                'title': "Too many attendees",
                'message': "Increase seats or remove excess attendees",
                },
            }


    #Validaciones a los campos (constraints)
    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("A session's instructor can't be an attendee")


    #Function para calcular la fecha de fin del curso
    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            start = fields.Datetime.from_string(r.start_date)
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = start + duration


    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue

            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            start_date = fields.Datetime.from_string(r.start_date)
            end_date = fields.Datetime.from_string(r.end_date)
            r.duration = (end_date - start_date).days + 1

    #Funcion para calcular la duracion de  
    #la sesiones de dias a horas
    @api.depends('duration')
    def _get_hours(self):
        for r in self:
            r.hours = r.duration * 24

    def _set_hours(self):
        for r in self:
            r.duration = r.hours / 24


    #Función para calcular cuantas personas
    #hay en un curso.
    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)
