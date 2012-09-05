#-*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import logout
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import messages
from django.conf import settings
import models
import forms
import pagseguro
from email import enviar_email



def user_is_coordenador(f):
    return user_passes_test(lambda u: hasattr(u, 'coordenador'))(f)



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
            messages.error(request, u"Nenhum usuário com o email {} informado foi encontrado.".format(email))
            email = None

    return render_to_response("recuperar_senha.html", 
                              RequestContext(request, {"email": email}))



@user_is_coordenador
def editar_juventude(request):
    form = forms.EditarJuventude(instance=request.user.coordenador.juventude)

    return render_to_response('coordenador/editar_juventude.html', 
                              RequestContext(request, {'form' : form}))



@user_is_coordenador
def salvar_juventude(request):
    form = forms.EditarJuventude(request.POST, instance=request.user.coordenador.juventude)

    if form.is_valid():
        form.save()
        messages.add_message(request, messages.INFO, "Dados da juventude salvos com sucesso!")
        return HttpResponseRedirect("/coordenador/editar_juventude")
    else:
        return render_to_response('/coordenador/editar_juventude.html', 
                                  RequestContext(request, {'form' : form}))



@user_is_coordenador
def novo_confraternista(request):
    juventude = request.user.coordenador.juventude
    
    convites_disponiveis = (juventude.limite_confraternistas -
                            juventude.codigos_cadastro.count() - 
                            juventude.confraternistas.count())

    return render_to_response("coordenador/listar_codigos.html",
                              RequestContext(request, {'codigos' : juventude.codigos_cadastro.all(),
                                                       'form': forms.ConviteConfraternista(),
                                                       'convites_disponiveis': convites_disponiveis}))



@user_is_coordenador
def criar_codigo_cadastro(request):
    juventude = request.user.coordenador.juventude

    form = forms.ConviteConfraternista(request.POST)
    
    if juventude.confraternistas.count() + juventude.codigos_cadastro.count() >= \
       juventude.limite_confraternistas:
        messages.add_message(request, messages.ERROR, 
            "O limite de confraternistas da sua Juventude Espírita foi atingido.\n"
            "Caso queira cadastrar outros confraternistas, entre em contato com a coordenação geral.")
    elif form.is_valid():
        email = form.cleaned_data["email"]
        nome = form.cleaned_data["nome"]

        codigo = models.CodigoCadastro(juventude=juventude, confraternista=True, coordenador=False, email=email, nome=nome)
        codigo.save()

        try:
            enviar_email(email, 
                         u"Convite para inscrição na COMEBH Noroeste 2013", 
                         "mail/confraternista_convidado.html",
                         {'nome' : nome, 'url': settings.SITE_URL, 'codigo': codigo.codigo})
        except Exception as e:
            print e
            codigo.delete()
            messages.add_message(request, messages.ERROR, "Erro ao enviar email. Verifique o email digitado e tente novamente.")

        else:
            messages.add_message(request, messages.INFO, "Confraternista convidado com sucesso!")        
            messages.add_message(request, messages.INFO, u"Foi enviado um email a {} com informações sobre o cadastro.".format(email))
    else:
        messages.add_message(request, messages.ERROR, u"É necessário informar nome e email para convidar um confraternista.")

    return HttpResponseRedirect("/coordenador/novo_confraternista")



@user_passes_test(lambda u: u.is_staff)
def ver_convites_coordenador(request):
    codigos = models.CodigoCadastro.objects.filter(coordenador=True)
    form = forms.ConviteCoordenador()

    return render_to_response("administrador/listar_codigos.html", 
                              RequestContext(request, {"codigos": codigos,
                                                       "form": form}))



@user_passes_test(lambda u: u.is_staff)
def desfazer_convite_coordenador(request):
    codigo = models.CodigoCadastro.objects.get(codigo=int(request.GET["codigo"]))

    if codigo:
        codigo.delete()

    messages.add_message(request, messages.INFO, "Convite apagado com sucesso!")
    return HttpResponseRedirect("/administrador/convites_coordenador")


@user_passes_test(lambda u: u.is_staff)
def convidar_coordenador(request):
    juventude = models.JuventudeEspirita.objects.get(id=int(request.POST["juventude"]))

    form = forms.ConviteCoordenador(request.POST)

    if not form.is_valid():
      messages.add_message(request, messages.ERROR, u"Por favor, preencha todos os campos para convidar o coordenador.")
    else:
      email = form.cleaned_data["email"]
      nome = form.cleaned_data["nome"]
      is_confraternista = form.cleaned_data["is_confraternista"]

      codigo = models.CodigoCadastro(juventude=juventude, coordenador=True, confraternista=is_confraternista, email=email, nome=nome)
      codigo.save()

      try:
          enviar_email(email, 
                       u"Convite para coordenador de Juventude Espírita na COMEBH Noroeste 2013", 
                       "mail/coordenador_convidado.html",
                       {'nome' : nome, 'juventude': juventude.nome, 'url': settings.SITE_URL, 'codigo': codigo.codigo})
      except Exception as e:
          print e
          codigo.delete()
          messages.add_message(request, messages.ERROR, "Erro ao enviar email. Verifique o email digitado e tente novamente.")

      else:
          messages.add_message(request, messages.INFO, "Coordenador convidado com sucesso!")        
          messages.add_message(request, messages.INFO, u"Foi enviado um email a {} com informações sobre o cadastro.".format(email))
      
    return HttpResponseRedirect("/administrador/convites_coordenador")



@user_is_coordenador
def desfazer_convite(request):
    codigo = models.CodigoCadastro.objects.get(juventude=request.user.coordenador.juventude,
                                                  codigo=int(request.GET["codigo"]))
    if codigo:
        codigo.delete()

    messages.add_message(request, messages.INFO, "Convite apagado com sucesso!")
    return HttpResponseRedirect("/coordenador/novo_confraternista")



@user_is_coordenador
def listar_confraternistas(request):
    confraternistas = models.Confraternista.objects.filter(juventude=request.user.coordenador.juventude)

    return render_to_response("coordenador/listar_confraternistas.html", 
                              RequestContext(request, {"confraternistas": confraternistas,
                                                       "juventude": request.user.coordenador.juventude}))



@user_is_coordenador
def autorizar_confraternista(request):
    confraternista = models.Confraternista.objects.get(id=request.GET.get("id"))

    if not confraternista or confraternista.juventude != request.user.coordenador.juventude:
        return HttpResponseForbidden()

    confraternista.autorizado = True

    enviar_email(confraternista.usuario.email,
                 u"Seus dados de inscrição na COMEBH 2013 foram aprovados",
                 "mail/confraternista_aprovado.html",
                 {'nome': confraternista.usuario.first_name})

    confraternista.save()

    messages.add_message(request, messages.INFO, "Confraternista autorizado!")
    return HttpResponseRedirect("/coordenador/listar_confraternistas")



def novo_usuario(request):

    id_codigo = request.GET.get("codigo")

    if id_codigo and id_codigo.isdigit() and models.CodigoCadastro.objects.filter(codigo=int(id_codigo)).count():
        codigo_cadastro = models.CodigoCadastro.objects.get(codigo=int(id_codigo))
        form = forms.NovoUsuario(initial={'nome':   codigo_cadastro.nome, 
                                          'email':  codigo_cadastro.email,
                                          'codigo': codigo_cadastro.codigo})
            
    elif request.method == 'POST':
        form = forms.NovoUsuario(request.POST)
    else:
        messages.add_message(request, messages.ERROR, u"É necessário um convite para se cadastrar.")
        return HttpResponseRedirect("/")

    if not id_codigo and form.is_valid():
            usuario = User()
            usuario.username = form.cleaned_data['login']
            usuario.set_password(form.cleaned_data['senha'])
            usuario.email = form.cleaned_data['email']

            nomes = form.cleaned_data['nome'].split(" ")

            usuario.first_name = nomes[0]
            usuario.last_name = " ".join(nomes[1:])

            codigo = models.CodigoCadastro.objects.get(codigo=form.cleaned_data['codigo'])

            usuario.save()

            if codigo.coordenador:
                coord = models.Coordenador()
                coord.usuario = usuario
                coord.juventude = codigo.juventude
                coord.save()
            
            if codigo.confraternista:
                conf = models.Confraternista()
                conf.usuario = usuario
                conf.juventude = codigo.juventude
                conf.save()

            codigo.delete()

            messages.add_message(request, messages.INFO, u"Seu cadastro foi realizado! Você pode fazer login agora.")
            return HttpResponseRedirect("/")
    
    return render_to_response("cadastro.html", 
            RequestContext(request, {"form": form}))



@user_is_coordenador
def adicionar_inscricao_pagamento(request):
  conf_id = int(request.GET.get("id"))

  confraternista = models.Confraternista.objects.get(id=conf_id)

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

    is_coordenador = hasattr(request.user, 'coordenador')
    is_confraternista = hasattr(request.user, 'confraternista')

    conf = None

    mostrar_link_autorizacao = False

    if is_coordenador and conf_id is not None:
        confraternista = models.Confraternista.objects.get(id=int(conf_id))

        if confraternista.juventude != request.user.coordenador.juventude:
          return HttpResponseForbidden()

        if not confraternista.autorizado:
            mostrar_link_autorizacao = True

    else:
        confraternista = request.user.confraternista

        if confraternista.autorizado and request.method == 'POST':
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

        if is_coordenador:
            confraternista.autorizado = True

        confraternista.save()
        messages.add_message(request, messages.INFO, "Dados de inscrição salvos com sucesso!")

        if is_confraternista and request.user.confraternista == confraternista:

            enviar_email(request.user.email, 
                         u"Seus dados de inscrição foram salvos",
                         "mail/confraternista_aguardar_aprovacao.html",
                         {'confraternista': request.user.confraternista})

            enviar_email([c.usuario.email for c in request.user.confraternista.juventude.coordenadores.all()],
                         u"{} preencheu seus dados de inscrição".format(request.user.confraternista.usuario.first_name),
                         "mail/coordenador_aprovar_confraternista.html",
                         {'nome': request.user.get_full_name(), 'url': settings.SITE_URL})

            messages.add_message(request, messages.INFO, "Verifique seu email para mais informações.")

        return HttpResponseRedirect("/")

    return render_to_response("confraternista/editar_dados.html",
                              RequestContext(request, 
                                             {"form": form,
                                              "id": conf_id,
                                              "juventude": request.user.confraternista.juventude 
                                                           if is_confraternista
                                                           else request.user.coordenador.juventude,
                                              "nome": confraternista.usuario.get_full_name(),
                                              "mostrar_link_autorizacao": mostrar_link_autorizacao}))


def imprimir_autorizacao_pais(request):

    if request.GET.get("id"):
        confraternista = models.Confraternista.objects.get(id=int(request.GET.get("id")))
    else:
        confraternista = request.user.confraternista

    print "Confraternista: ", confraternista.usuario.get_full_name()

    return render_to_response("confraternista/autorizacao.html", 
                              RequestContext(request, {"confraternista": confraternista}))



@user_is_coordenador
def imprimir_autorizacao_casa_espirita(request):
    juventude = request.user.coordenador.juventude
    confraternistas = models.Confraternista.objects.filter(juventude=juventude)

    return render_to_response("coordenador/autorizacao.html",
                              RequestContext(request, {"confraternistas": confraternistas,
                                                       "juventude": juventude}))



def confraternista_realizar_pagamento(request):
  url = pagseguro.gerar_pagamento([request.user.confraternista], request.user)
  return HttpResponseRedirect(url)
