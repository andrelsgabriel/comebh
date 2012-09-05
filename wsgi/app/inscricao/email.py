# -*- coding: utf-8 -*-
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context

def enviar_email(destinatarios, assunto, template, contexto={}, cc=[], bcc=[]):
    texto = get_template(template).render(Context(contexto))

    if type(destinatarios) not in (list, tuple):
        destinatarios = (destinatarios,)

    m = EmailMessage(subject=assunto, body=texto, to=destinatarios, cc=cc, bcc=bcc)
    m.content_subtype = "html"
    m.send()