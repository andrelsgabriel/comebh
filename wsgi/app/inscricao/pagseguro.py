#-*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
import models
import urllib
import urllib2
import xml.etree.ElementTree as ET

INSCRICAO_COM_CAMISA = {"id": 1, "descricao": "Inscrição na COMEBH 2013 + Camisa", "valor": settings.VALOR_INSCRICAO + settings.VALOR_CAMISA}
INSCRICAO_SEM_CAMISA = {"id": 2, "descricao": "Inscrição na COMEBH 2013", "valor": settings.VALOR_INSCRICAO}

PRODUTOS = (INSCRICAO_COM_CAMISA, INSCRICAO_SEM_CAMISA)

URL_PAGAMENTO = "https://ws.pagseguro.uol.com.br/v2/checkout"
URL_FLUXO_PAGAMENTO = "https://pagseguro.uol.com.br/v2/checkout/payment.html?code="
URL_NOTIFICACAO = "https://ws.pagseguro.uol.com.br/v2/transactions/notifications/"



def url_fluxo_pagamento(codigo):
	return URL_FLUXO_PAGAMENTO + codigo



def url_notificacao(codigo):
	return URL_NOTIFICACAO + codigo



def gerar_pagamento(confraternistas, usuario):

	n_inscricoes_camisa = len([1 for c in confraternistas if c.tamanho_camisa])
	n_inscricoes_sem_camisa = len(confraternistas) - n_inscricoes_camisa

	dadosPagamento = {"email": settings.PAGSEGURO_EMAIL_CONTA,
			 "token": settings.PAGSEGURO_TOKEN,
		 	 "currency": "BRL"}

	iid = 1

	pagamento = models.Pagamento()
	pagamento.valor_bruto = n_inscricoes_camisa * INSCRICAO_COM_CAMISA["valor"] + \
					  		n_inscricoes_sem_camisa * INSCRICAO_SEM_CAMISA["valor"]
	pagamento.save()

	for c in confraternistas:
		c.pagamento_inscricao = pagamento
		c.save()

	if n_inscricoes_camisa:
		siid = str(iid)
		dadosPagamento["itemId" + siid] = INSCRICAO_COM_CAMISA["id"]
		dadosPagamento["itemDescription" + siid] = INSCRICAO_COM_CAMISA["descricao"]
		dadosPagamento["itemAmount" + siid] = "{0:.2f}".format(INSCRICAO_COM_CAMISA["valor"])
		dadosPagamento["itemQuantity" + siid] = n_inscricoes_camisa
		iid += 1

	if n_inscricoes_sem_camisa:
		siid = str(iid)
		dadosPagamento["itemId" + siid] = INSCRICAO_SEM_CAMISA["id"]
		dadosPagamento["itemDescription" + siid] = INSCRICAO_SEM_CAMISA["descricao"]
		dadosPagamento["itemAmount" + siid] = "{0:.2f}".format(INSCRICAO_SEM_CAMISA["valor"])
		dadosPagamento["itemQuantity" + siid] = n_inscricoes_sem_camisa
		iid += 1

	dadosPagamento["reference"] = str(pagamento.id)
	#dadosPagamento["senderName"] = usuario.get_full_name().encode("utf-8")
	dadosPagamento["senderEmail"] = usuario.email

	print urllib.urlencode(dadosPagamento).encode("utf-8")

	try:
		xml = urllib2.urlopen(
						urllib2.Request(URL_PAGAMENTO,
								headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
							  	data=urllib.urlencode(dadosPagamento).encode("utf-8"))).read()
	except Exception as e:
		import traceback; traceback.print_exc(e)
		raise

	root = ET.fromstring(xml)
	codigo = root.find("code").text

	return url_fluxo_pagamento(codigo)



@csrf_exempt
def processar_notificacao(request):
	codigo = request.POST.get("notificationCode")

	r = urllib.urlopen(url_notificacao(codigo) + "?" + 
						urllib.urlencode({'email': settings.PAGSEGURO_EMAIL_CONTA,
										  'token': settings.PAGSEGURO_TOKEN}))

	xml = r.read()

	print "Recebido do PagSeguro: ", xml

	root = ET.fromstring(xml)

	id_pagamento = int(root.find("reference").text)
	pagamento = models.Pagamento.objects.get(id=id_pagamento)

	pagamento.transacao_pagseguro = root.find("code").text
	pagamento.estado = int(root.find("status").text)
	pagamento.valor_bruto = Decimal(root.find("grossAmount").text)
	pagamento.valor_liquido = Decimal(root.find("netAmount").text)

	pagamento.save()

	return HttpResponse(u"Notificação processada.")
