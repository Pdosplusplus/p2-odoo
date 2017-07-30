# -*- coding: utf-8 -*-

from datetime import datetime, date
from dateutil import rrule

FORMA_DATE="%Y-%m-%d"

def compareMounts(dateone, datetwo):

	date_two = datetime.strptime(str(datetwo), FORMA_DATE)

	if str(dateone) == str(date_two.month):

		return True

	return False

def years(dateone):

	fecha = datetime.strptime(dateone,  FORMA_DATE)

	today = datetime.now().date()

	today = datetime.strptime(str(today), FORMA_DATE)

	diferencia = today - fecha

	return diferencia.days / 365


def workDays(start_date):
        
	feriados= 5, 6

	laborales = [dia for dia in range(7) if dia not in feriados]

	end_date = datetime.now().date()

	date_ini = datetime.strptime(str(start_date), FORMA_DATE)

	date_fin = datetime.strptime(str(end_date), FORMA_DATE)

	totalDias= rrule.rrule(rrule.DAILY,
						dtstart=date_ini, 
						until=date_fin, 
						byweekday=laborales)

	return totalDias.count()