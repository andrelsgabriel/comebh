# -*- coding: utf-8 -*-
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.core.mail import EmailMessage
from django.core import mail
import models
import urllib
import urllib2
import traceback
import random


def enviar_email_juventudeespirita(destinatarios, assunto, template, contexto={}, cc=[], bcc=[]):
    contextoComebh = {"comebh": models.Comebh.comebh_vigente()}

    texto = get_template(template).render(Context(dict(contextoComebh.items() + contexto.items())))

    if type(destinatarios) not in (list, tuple):
        destinatarios = (destinatarios,)

    print u"Enviando email {0} para {1}".format(template, u",".join(destinatarios))

    data = urllib.urlencode({'from': settings.DEFAULT_FROM_EMAIL,
                             'from_name': settings.EMAIL_FROM_NAME,
                             'to': ",".join(destinatarios),
                             'subject': assunto.encode("utf-8"),
                             'message': texto.encode("utf-8"),
                             'cc': ",".join(cc),
                             'bcc': ",".join(bcc),
                             'token': settings.EMAIL_TOKEN})

    log = urllib2.urlopen(urllib2.Request(settings.EMAIL_REMOTE_SENDER,
                          headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
                          data=data.encode("utf-8")
                          )).read()

    print "Log: ", log
    return True

def enviar_email(destinatarios, assunto, template, contexto={}, cc=[], bcc=[]):
    contextoComebh = {"comebh": models.Comebh.comebh_vigente()}

    texto = get_template(template).render(Context(dict(contextoComebh.items() + contexto.items())))

    if type(destinatarios) not in (list, tuple):
        destinatarios = (destinatarios,)

    print u"Enviando email {0} para {1}".format(template, u",".join(destinatarios))

    from_address = random.choice(settings.ALTERNATE_EMAILS)

    try:
        connection = mail.get_connection(username=from_address)
        m = EmailMessage(assunto.encode("utf-8"),
                         texto.encode("utf-8"),
                         from_address,
                         destinatarios,
                         bcc=cc+bcc,
                         connection=connection)
        m.content_subtype = "html"
        result = connection.send_messages([m])
        return result
    except Exception as e:
        traceback.print_exc(e)
        raise
