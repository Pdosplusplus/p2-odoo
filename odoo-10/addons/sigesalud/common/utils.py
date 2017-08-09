# -*- coding: utf-8 -*-

import smtplib
from datetime import datetime, date
from dateutil import rrule
from email.MIMEText import MIMEText

#EMITTER = os.environ['EMITTER']
#PASSWD_MAIL = os.environ['PASSWDMAIL']
FORMA_DATE="%Y-%m-%d"
EMITTER ="vpino.geekos@test.com"
PASSWD_MAIL="...."

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

def diff_days():
        
	start_date = datetime.now().date()

	end_date = "2018-03-10"

	date_ini = datetime.strptime(str(start_date), FORMA_DATE)

	date_fin = datetime.strptime(str(end_date), FORMA_DATE)

	totalDias= rrule.rrule(rrule.DAILY,
						dtstart=date_ini, 
						until=date_fin)

	return totalDias.count()


def sendEmail(addressee, info, emitter=None):

	message_template = """\
El Reembolso de id <strong> %(id)s </strong> del titular: <strong> %(name)s </strong> 
a la fecha de: <strong> %(date)s </strong> ya cumplio los 40 dias de fecha limite 
que tiene el seguro para cancelarlo. Se le agradece a los ADMINISTRADORES verificar 
el caso y solventarlo a la mayor brevedad posible.

Sistema de Alertas SIGESALUD.

<a link="geekos.co.ve"> Cooperativa Geekos <a/>
""" % info

	# Mail Struct
	email = MIMEText(message_template)
	email['From'] = EMITTER
	email['To'] = addressee
	email['Subject'] = "Alerta de Reembolso :: HCM-SIGESALUD"

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
	