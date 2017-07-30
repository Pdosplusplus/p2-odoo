# -*- coding: utf-8 -*-

from datetime import datetime, date

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