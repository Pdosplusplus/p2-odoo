# -*- coding: utf-8 -*-

from datetime import datetime, date

FORMA_DATE="%Y-%m-%d"

def compareMounts(dateone, datetwo):

	date_two = datetime.strptime(str(datetwo), FORMA_DATE)

	if str(dateone) == str(date_two.month):

		return True

	return False
