# -*- coding: utf-8 -*-

import smtplib 
from datetime import datetime, date
from dateutil import rrule
from email.MIMEText import MIMEText

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

def sendEmail( addressee, info, emitter=None):

	if emitter is None:
		emitter = 'agilis.report@gmail.com'
		password= '#'
	
	message_template = """\
El proyecto <strong> %(name)s </strong> tiene fecha de culminuacion <br>
de %(end_date)s y tiene como dias planificados <strong> %(days_plan)s </strong> <br>
de los cuales solo se han ejecutado <strong> %(days_exe)s </strong> se agradece <br>
tomar todas las medidas necesarias para cumplir con los objetivos previstos. <br>

Sistema de Alertas AGILIS.

<a link="geekos.co.ve"> Cooperativa Geekos <a/>
""" % info

	# Mail Struct
	email = MIMEText(message_template)
	email['From'] = emitter
	email['To'] = addressee
	email['Subject'] = "Alerta de Avance :: CFG-AGILIS"

	try:
		
		# Server SMTP Gmail 
		serverSMTP = smtplib.SMTP(host='smtp.gmail.com', port=587)
		serverSMTP.ehlo() 
		serverSMTP.starttls() 
		serverSMTP.ehlo() 
		serverSMTP.login(emitter, password)

		# Send mail
		serverSMTP.sendmail(emitter, addressee, email.as_string()) 

		# Close conexion
		serverSMTP.close()

	except Exception as e:
		
		return e
	
	