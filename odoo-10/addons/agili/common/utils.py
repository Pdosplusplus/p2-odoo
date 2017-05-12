# -*- coding: utf-8 -*-

from datetime import datetime, date
from dateutil import rrule

FORMA_DATE="%Y-%m-%d"

def workDays(start_date, end_date):
        
	feriados= 5, 6

	laborales = [dia for dia in range(7) if dia not in feriados]
	
	date_ini = datetime.strptime(str(start_date), FORMA_DATE)

	date_fin = datetime.strptime(str(end_date), FORMA_DATE)

	totalDias= rrule.rrule(rrule.DAILY,
						dtstart=date_ini, 
						until=date_fin, 
						byweekday=laborales)

	return totalDias.count()

def validKey(array, key):

    try:

        print "No es posible"
        return array[key]

    except KeyError as e:
        
        print e

        return 0