# -*- coding: utf-8 -*-

import smtplib
import os 
from datetime import datetime, date
from dateutil import rrule
from email.MIMEText import MIMEText

#EMITTER = os.environ['EMITTER']
#PASSWD_MAIL = os.environ['PASSWDMAIL']
FORMA_DATE="%Y-%m-%d"
EMITTER ="SABE"
PASSWD_MAIL="vpino.geekos"
DAYS_LESS = '2017-12-31'
DAYS_HIGHER = '2017-01-01'

def compareDates(dateone, datetwo, operation):

	date_one = datetime.strptime(str(dateone), FORMA_DATE)
	date_two = datetime.strptime(str(datetwo), FORMA_DATE)

	if operation == 'higher':

		if str(date_one) > str(date_two):

			return True

	else:

		if str(date_one) < str(datetwo):

			return True

	return False

def daysExe(date):

	fecha = datetime.now().date()

	today = datetime.strptime(str(fecha), FORMA_DATE)
	date_give = datetime.strptime(str(date), FORMA_DATE)

	exe = date_give - today

	if exe.days < 0:

		exe = exe.days * -1

		return int(exe)

	return int(exe.days)

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

def sendEmail(addressee, info, emitter=None):

	message_template = """\
El proyecto <strong> %(name)s </strong> tiene fecha de culminuacion
de %(end_date)s y tiene como dias planificados <strong> %(days_plan)s </strong>
de los cuales solo se han ejecutado <strong> %(days_exe)s </strong> se agradece
tomar todas las medidas necesarias para cumplir con los objetivos previstos.

Sistema de Alertas AGILIS.

<a link="geekos.co.ve"> Cooperativa Geekos <a/>
""" % info

	# Mail Struct
	email = MIMEText(message_template)
	email['From'] = EMITTER
	email['To'] = addressee
	email['Subject'] = "Alerta de Avance :: CFG-AGILIS"

	try:
		
		# Server SMTP Gmail 
		serverSMTP = smtplib.SMTP(host='smtp.gmail.com', port=587)
		serverSMTP.ehlo() 
		serverSMTP.starttls() 
		serverSMTP.ehlo() 
		serverSMTP.login(EMITTER, PASSWD_MAIL)

		# Send mail
		serverSMTP.sendmail(EMITTER, addressee, email.as_string()) 

		# Close conexion
		serverSMTP.close()

	except Exception as e:
		
		return e
	
	