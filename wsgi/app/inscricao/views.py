#-*- coding: utf-8 -*-

import datetime
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import logout
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import messages
from django.conf import settings
from models import *
import sys
import forms
import pagseguro
from email import enviar_email
from decimal import Decimal


def process_context(request):
    return {"coordenador": Coordenador.do_usuario(request.user),
            "confraternista": Confraternista.do_usuario(request.user)}


def user_is_coordenador(f):
    return user_passes_test(lambda u: Coordenador.do_usuario(u))(f)


@login_required
def principal(request):
    return render_to_response('principal.html', RequestContext(request))



@login_required
def sair(request):
    logout(request)
    return HttpResponseRedirect("/")


def recuperar_senha(request):

    email = None

    if request.method == 'POST' and request.POST.get("email"):
        email = request.POST["email"]
        usuarios = User.objects.filter(email=email)

        if usuarios:
            u = usuarios[0]
            senha = User.objects.make_random_password()
            u.set_password(senha)
            u.save()

            enviar_email(u.email, u"Recuperação de senha", "mail/recuperar_senha.html",
                        {"usuario": u, "senha": senha})
        else:
            messages.error(request, u"Nenhum usuário com o email {0} informado foi encontrado.".format(email))
            email = None

    return render_to_response("recuperar_senha.html",
                              RequestContext(request, {"email": email}))



def editar_usuario(request):

    if request.method == 'POST':
        form = forms.AlterarUsuario(request.POST)

        if form.is_valid():
            request.user.email = form.cleaned_data["email"]

            if form.cleaned_data["senha"]:
                request.user.set_password(form.cleaned_data["senha"])

            nomes = form.cleaned_data["nome"].split(u" ")
            request.user.first_name = nomes[0]
            request.user.last_name = u" ".join(nomes[1:])
            request.user.save()
            messages.info(request, u"Dados alterados com sucesso!")

    else:
        form = forms.AlterarUsuario(initial={"nome": request.user.get_full_name(),
                                             "email": request.user.email})

    return render_to_response("editar_usuario.html",
                              RequestContext(request, {"form": form}))



@user_is_coordenador
def editar_juventude(request):
    form = forms.EditarJuventude(instance=Coordenador.do_usuario(request.user).juventude)

    return render_to_response('coordenador/editar_juventude.html',
                              RequestContext(request, {'form' : form}))



@user_is_coordenador
def salvar_juventude(request):
    form = forms.EditarJuventude(request.POST, instance=Coordenador.do_usuario(request.user).juventude)

    if form.is_valid():
        form.save()
        messages.add_message(request, messages.INFO, "Dados da juventude salvos com sucesso!")
        return HttpResponseRedirect("/coordenador/editar_juventude")
    else:
        return render_to_response('coordenador/editar_juventude.html',
                                  RequestContext(request, {'form' : form}))



@user_is_coordenador
def novo_confraternista(request):
    juventude = Coordenador.do_usuario(request.user).juventude

    convites_disponiveis = (juventude.limite_confraternistas -
                            juventude.codigos_cadastro.count() -
                            juventude.confraternistas.filter(comebh=Comebh.comebh_vigente()).count())

    return render_to_response("coordenador/listar_codigos.html",
                              RequestContext(request, {'codigos' : juventude.codigos_cadastro.all(),
                                                       'form': forms.ConviteConfraternista(),
                                                       'convites_disponiveis': max(0, convites_disponiveis),
                                                       'ano_comebh': Comebh.comebh_vigente().ano()}))



def enviar_convite_confraternista(request, codigo):
    enviar_email(codigo.email,
                 u"Convite para inscrição na COMEBH Noroeste {0}"
                 .format(Comebh.comebh_vigente().ano()),
                 "mail/confraternista_convidado.html",
                 {'nome' : codigo.nome, 'url': settings.SITE_URL, 'codigo': codigo.codigo})

    messages.add_message(request, messages.INFO, "Confraternista convidado com sucesso!")
    messages.add_message(request, messages.INFO, u"Foi enviado um email a {0} com informações sobre o cadastro.".format(codigo.email))



@user_is_coordenador
def criar_codigo_cadastro(request):
    juventude = Coordenador.do_usuario(request.user).juventude

    form = forms.ConviteConfraternista(request.POST)

    if juventude.confraternistas.filter(comebh=Comebh.comebh_vigente()).count() + \
       juventude.codigos_cadastro.count() >= juventude.limite_confraternistas:
        messages.add_message(request, messages.ERROR,
            "O limite de confraternistas da sua Juventude Espírita foi atingido.\n"
            "Caso queira cadastrar outros confraternistas, entre em contato com a coordenação geral.")
    elif form.is_valid():
        email = form.cleaned_data["email"]
        nome = form.cleaned_data["nome"]

        codigo = CodigoCadastro(juventude=juventude, confraternista=True, coordenador=False, email=email, nome=nome)
        codigo.save()

        try:
            enviar_convite_confraternista(request, codigo)
        except Exception as e:
            import traceback
            traceback.print_exc(e)
            codigo.delete()
            messages.add_message(request, messages.ERROR, "Erro ao enviar email. Verifique o email digitado e tente novamente.")
    else:
        messages.add_message(request, messages.ERROR, u"É necessário informar nome e email para convidar um confraternista.")

    return HttpResponseRedirect("/coordenador/novo_confraternista")



@user_is_coordenador
def reenviar_email_convite(request):
    codigo = CodigoCadastro.objects.get(codigo=int(request.GET["codigo"]))

    try:
        enviar_convite_confraternista(request, codigo)
    except Exception as e:
        messages.add_message(request, messages.ERROR, "Erro ao enviar email. Verifique o email digitado e tente novamente.")

    return HttpResponseRedirect("/coordenador/novo_confraternista")



@user_passes_test(lambda u: u.is_staff)
def ver_convites_coordenador(request):
    codigos = CodigoCadastro.objects.filter(coordenador=True)
    form = forms.ConviteCoordenador()

    return render_to_response("administrador/listar_codigos.html",
                              RequestContext(request, {"codigos": codigos,
                                                       "form": form,
                                                       "ano_comebh": Comebh.comebh_vigente().ano()}))



@user_passes_test(lambda u: u.is_staff)
def desfazer_convite_coordenador(request):
    codigo = CodigoCadastro.objects.get(codigo=int(request.GET["codigo"]))

    if codigo:
        codigo.delete()

    messages.add_message(request, messages.INFO, "Convite apagado com sucesso!")
    return HttpResponseRedirect("/administrador/convites_coordenador")



def enviar_convite_coordenador(request, codigo):
  enviar_email(codigo.email,
               u"Convite para coordenador de Juventude Espírita na COMEBH Noroeste {0}"
               .format(Comebh.comebh_vigente().ano()),
               "mail/coordenador_convidado.html",
               {'nome' : codigo.nome, 'juventude': codigo.juventude.nome,
                'url': settings.SITE_URL, 'codigo': codigo.codigo})



@user_passes_test(lambda u: u.is_staff)
def convidar_coordenador(request):
    juventude = JuventudeEspirita.objects.get(id=int(request.POST["juventude"]))

    form = forms.ConviteCoordenador(request.POST)

    if not form.is_valid():
      messages.add_message(request, messages.ERROR, u"Por favor, preencha todos os campos para convidar o coordenador.")
    else:
      email = form.cleaned_data["email"]
      nome = form.cleaned_data["nome"]

      codigo = CodigoCadastro(juventude=juventude, coordenador=True, email=email, nome=nome)
      codigo.save()

      try:
          enviar_convite_coordenador(request, codigo)
      except Exception as e:
          import traceback
          traceback.print_exc(e)
          codigo.delete()
          messages.add_message(request, messages.ERROR, "Erro ao enviar email. Verifique o email digitado e tente novamente.")

      else:
          messages.add_message(request, messages.INFO, "Coordenador convidado com sucesso!")
          messages.add_message(request, messages.INFO, u"Foi enviado um email a {0} com informações sobre o cadastro.".format(email))

    return HttpResponseRedirect("/administrador/convites_coordenador")



@user_passes_test(lambda u: u.is_staff)
def reenviar_convite_coordenador(request):
  try:
    codigo = CodigoCadastro.objects.get(codigo=int(request.GET.get("codigo")))
    enviar_convite_coordenador(request, codigo)
    messages.info(request, "Convite reenviado!")
  except:
    messages.error(request, "Erro interno ao reenviar convite.")

  return HttpResponseRedirect("/administrador/convites_coordenador")



@user_is_coordenador
def desfazer_convite(request):
    codigo = CodigoCadastro.objects.get(juventude=Coordenador.do_usuario(request.user).juventude,
                                                  codigo=int(request.GET["codigo"]))
    if codigo:
        codigo.delete()

    messages.add_message(request, messages.INFO, "Convite apagado com sucesso!")
    return HttpResponseRedirect("/coordenador/novo_confraternista")



@user_is_coordenador
def listar_confraternistas(request):
    confraternistas = Confraternista.objects.filter(juventude=Coordenador.do_usuario(request.user).juventude,
                                                           comebh=Comebh.comebh_vigente())

    return render_to_response("coordenador/listar_confraternistas.html",
                              RequestContext(request, {"confraternistas": confraternistas,
                                                       "juventude": Coordenador.do_usuario(request.user).juventude}))



@user_is_coordenador
def autorizar_confraternista(request):
    confraternista = Confraternista.objects.get(id=request.GET.get("id"))

    if not confraternista or confraternista.juventude != Coordenador.do_usuario(request.user).juventude:
        return HttpResponseForbidden()

    confraternista.autorizado = True

    enviar_email(confraternista.usuario.email,
                 u"Seus dados de inscrição na COMEBH {0} foram aprovados"
                 .format(Comebh.comebh_vigente().ano()),
                 "mail/confraternista_aprovado.html",
                 {'nome': confraternista.usuario.first_name})

    confraternista.save()

    messages.add_message(request, messages.INFO, "Confraternista autorizado!")
    return HttpResponseRedirect("/coordenador/listar_confraternistas")



def novo_usuario(request):

    id_codigo = request.GET.get("codigo")

    coordenador = False

    if id_codigo and id_codigo.isdigit() and CodigoCadastro.objects.filter(codigo=int(id_codigo)).count():
        codigo_cadastro = CodigoCadastro.objects.get(codigo=int(id_codigo))
        form = forms.NovoUsuario(initial={'nome':   codigo_cadastro.nome,
                                          'email':  codigo_cadastro.email,
                                          'codigo': codigo_cadastro.codigo})
        coordenador = codigo_cadastro.coordenador
        sys.stderr.write("Novo usuário é coordenador?" + str(coordenador) + "\n")

    elif request.method == 'POST':
        form = forms.NovoUsuario(request.POST)
    else:
        messages.add_message(request, messages.ERROR, u"É necessário um convite para se cadastrar.")
        return HttpResponseRedirect("/")

    if not id_codigo and form.is_valid():

            email = str(form.cleaned_data["email"])

            if User.objects.filter(email=email).count() == 1:
                usuario = User.objects.get(email=email)
                ja_existia = True
            else:
                usuario = User()
                ja_existia = False

            sys.stderr.write("O usuário já existia?" + str(ja_existia) + "\n")

            usuario.username = form.cleaned_data['login']
            usuario.set_password(form.cleaned_data['senha'])
            usuario.email = form.cleaned_data['email']

            nomes = form.cleaned_data['nome'].split(" ")

            usuario.first_name = nomes[0]
            usuario.last_name = " ".join(nomes[1:])

            codigo = CodigoCadastro.objects.get(codigo=form.cleaned_data['codigo'])

            usuario.save()

            if not codigo.coordenador or request.POST.get('confraternista'):
                if (codigo.juventude.limite_confraternistas -
                    codigo.juventude.codigos_cadastro.count() -
                    codigo.juventude.confraternistas.filter(comebh=Comebh.comebh_vigente()).count()) < 0:
                    if codigo.coordenador:
                        messages.error(request, u"O limite de cadastros de confraternistas desta Juventude Espírita foi atingido. Entre em contato com a coordenação geral.")
                    else:
                        messages.error(request, u"O limite de cadastros de confraternistas desta Juventude Espírita foi atingido. Entre em contato com a coordenação de sua Juventude Espírita.")
                    if not ja_existia:
                        usuario.delete()
                    return HttpResponseRedirect("/")

                if ja_existia and Confraternista.objects.filter(usuario=usuario).count():
                    conf = Confraternista.objects.filter(usuario=usuario).order_by("-comebh__data_evento")[0]
                    conf.pagamento_inscricao = None
                    conf.autorizado = False
                    conf.tamanho_camisa = None
                    conf.pk = None
                    sys.stderr.write("O confraternista já existia.\n")
                else:
                    conf = Confraternista()

                conf.comebh = Comebh.comebh_vigente()
                conf.usuario = usuario
                conf.juventude = codigo.juventude
                conf.save()

            if codigo.coordenador:
                coord = Coordenador()
                coord.comebh = Comebh.comebh_vigente()
                coord.usuario = usuario
                coord.juventude = codigo.juventude
                coord.save()

            codigo.delete()

            messages.add_message(request, messages.INFO, u"Seu cadastro foi realizado! Você pode fazer login agora.")
            return HttpResponseRedirect("/")

    return render_to_response("cadastro.html", {"form": form, "coordenador": coordenador},
            context_instance=RequestContext(request))



@user_is_coordenador
def adicionar_inscricao_pagamento(request):
  conf_id = int(request.GET.get("id"))

  confraternista = Confraternista.objects.get(id=conf_id)

  request.session["cart"] = request.session.get("cart") or []
  request.session["cart"].append(confraternista)
  request.session["cart_total"] = (request.session.get("cart_total") or 0) + confraternista.valor_inscricao()

  return HttpResponseRedirect("/coordenador/listar_confraternistas")



@user_is_coordenador
def limpar_inscricoes(request):
  request.session["cart"] = []
  request.session["cart_total"] = 0
  return HttpResponseRedirect("/coordenador/listar_confraternistas")



@user_is_coordenador
def redirecionar_pagamento(request):
  url = pagseguro.gerar_pagamento(request.session.get("cart"), request.user)
  return HttpResponseRedirect(url)



def editar_dados(request):

    #id do confraternista, para o caso de o coordenador estar editando os dados
    conf_id = request.POST.get('id') if request.method == 'POST' else request.GET.get('id')

    print "Conf_ID: ", conf_id

    is_coordenador = Coordenador.do_usuario(request.user) is not None
    is_confraternista = Confraternista.do_usuario(request.user) is not None

    conf = None

    mostrar_link_autorizacao = False

    if is_coordenador and conf_id is not None and conf_id.isdigit():
        confraternista = Confraternista.objects.get(id=int(conf_id))

        if confraternista.juventude != Coordenador.do_usuario(request.user).juventude:
          return HttpResponseForbidden()

        if not confraternista.autorizado:
            mostrar_link_autorizacao = True

    else:
        confraternista = Confraternista.do_usuario(request.user)

        if confraternista.autorizado and request.method == 'POST' and not is_coordenador:
          messages.add_message(request, messages.ERROR, u"Seus dados já foram aprovados. Para alterá-los, contate a coordenação de sua Juventude Espírita.")
          return HttpResponseRedirect("/confraternista/editar_dados")

    form = (forms.InscricaoConfraternista(instance=confraternista)
            if request.method != 'POST'
            else forms.InscricaoConfraternista(request.POST))

    if form.is_valid():
        for attr in ["nome_cracha", "sexo", "data_nascimento", "identidade",
                     "ano_ingresso_mocidade", "comebhs_anteriores",
                     "logradouro", "bairro", "cidade",
                     "telefone", "contato_urgencia", "parentesco_contato_urgencia",
                     "telefone_contato_urgencia", "telefone2_contato_urgencia",
                     "dieta_especial", "uso_medicamento", "alergia",
                     "voluntario_manutencao", "tamanho_camisa"]:
            setattr(confraternista, attr, form.cleaned_data.get(attr) or None)

        if request.POST['r_comprar_camisa'] == '0':
            confraternista.tamanho_camisa = None

        if is_coordenador and is_confraternista and Confraternista.do_usuario(request.user) == confraternista:
            confraternista.autorizado = True

        confraternista.save()
        messages.add_message(request, messages.INFO, u"Dados de inscrição salvos com sucesso!")

        if is_confraternista and not is_coordenador and Confraternista.do_usuario(request.user) == confraternista:

            enviar_email(request.user.email,
                         u"Seus dados de inscrição foram salvos",
                         "mail/confraternista_aguardar_aprovacao.html",
                         {'confraternista': Confraternista.do_usuario(request.user)})

            enviar_email([c.usuario.email for c in Confraternista.do_usuario(request.user).juventude.coordenadores.all()],
                         u"{0} preencheu seus dados de inscrição".format(Confraternista.do_usuario(request.user).usuario.first_name),
                         "mail/coordenador_aprovar_confraternista.html",
                         {'nome': request.user.get_full_name(), 'url': settings.SITE_URL})

            messages.add_message(request, messages.INFO, u"Verifique seu email para mais informações.")

        return HttpResponseRedirect("/")

    return render_to_response("confraternista/editar_dados.html",
                              RequestContext(request,
                                             {"form": form,
                                              "id": conf_id,
                                              "juventude": Confraternista.do_usuario(request.user).juventude
                                                           if is_confraternista
                                                           else Coordenador.do_usuario(request.user).juventude,
                                              "nome": confraternista.usuario.get_full_name(),
                                              "mostrar_link_autorizacao": mostrar_link_autorizacao}))


def imprimir_autorizacao_pais(request):

    if request.GET.get("id"):
        confraternista = Confraternista.objects.get(id=int(request.GET.get("id")))
    else:
        confraternista = Confraternista.do_usuario(request.user)

    comebh = Comebh.comebh_vigente()

    return render_to_response("confraternista/autorizacao.html",
                                {"confraternista": confraternista,
                                 "ano_comebh": comebh.ano(),
                                 "data_inicio_comebh": comebh.data_evento.strftime("%d/%m/%Y"),
                                 "data_fim_comebh": (comebh.data_evento +
                                                    datetime.timedelta(days=4))
                                                    .strftime("%d/%m/%Y")},
                                RequestContext(request))



@user_is_coordenador
def imprimir_autorizacao_casa_espirita(request):
    juventude = Coordenador.do_usuario(request.user).juventude
    confraternistas = Confraternista.objects.filter(juventude=juventude,
                                                           comebh=Comebh.comebh_vigente())

    comebh = Comebh.comebh_vigente()

    return render_to_response("coordenador/autorizacao.html",
                              RequestContext(request,
                                {"confraternistas": confraternistas,
                                 "juventude": juventude,
                                 "ano_comebh": comebh.ano(),
                                 "data_inicio_comebh": comebh.data_evento.strftime("%d/%m/%Y"),
                                 "data_fim_comebh": (comebh.data_evento +
                                                     datetime.timedelta(days=4))
                                                     .strftime("%d/%m/%Y")}))



def confraternista_realizar_pagamento(request):
  url = pagseguro.gerar_pagamento([Confraternista.do_usuario(request.user)], request.user)
  return HttpResponseRedirect(url)



@user_passes_test(lambda u: u.is_staff)
def editar_comebh(request):
    form = forms.Comebh(instance=Comebh.comebh_vigente())

    return render_to_response("administrador/editar_comebh.html",
                              RequestContext(request, {"form": form}))


@user_passes_test(lambda u: u.is_staff)
def salvar_comebh(request):
    comebh_atual = Comebh.comebh_vigente()
    form = forms.Comebh(request.POST, instance=comebh_atual)

    if form.is_valid():
        form.save()
        messages.add_message(request, messages.INFO, u"Configurações da COMEBH salvas com sucesso!.")

    return render_to_response("administrador/editar_comebh.html",
                              RequestContext(request, {"form": form}))


@user_passes_test(lambda u: u.is_staff)
def criar_comebh(request):
    comebh_atual = Comebh.comebh_vigente()

    confraternistas_sem_comebh = Confraternista.objects.filter(comebh=None)
    coordenadores_sem_comebh = Coordenador.objects.filter(comebh=None)

    for c in confraternistas_sem_comebh:
        c.comebh = comebh_atual
        c.save()

    for c in coordenadores_sem_comebh:
        c.comebh = comebh_atual
        c.save()

    nova_comebh = Comebh()
    nova_comebh.data_evento = datetime.date.today()
    nova_comebh.valor_inscricao = Decimal("0.0")
    nova_comebh.valor_camisa = Decimal("0.0")
    nova_comebh.limite_inscricoes = 0
    nova_comebh.data_limite_inscricoes = nova_comebh.data_evento
    nova_comebh.idade_minima = 0

    nova_comebh.save()

    for j in JuventudeEspirita.objects.all():
      j.limite_confraternistas = 0
      j.save()

    return editar_comebh(request)
