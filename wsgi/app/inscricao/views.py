#-*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import messages
import models
import forms

def user_is_coordenador(f):
    return user_passes_test(lambda u: hasattr(u, 'coordenador'))(f)


@login_required
def principal(request):
    return render_to_response('principal.html', RequestContext(request))



@login_required
def sair(request):
    logout(request)
    return HttpResponseRedirect("/")



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
    
    return render_to_response("coordenador/listar_codigos.html",
                              RequestContext(request, {'codigos' : juventude.codigos_cadastro.all()}))



@user_is_coordenador
def criar_codigo_cadastro(request):
    juventude = request.user.coordenador.juventude
    
    print "Limite:", juventude.limite_confraternistas

    if juventude.confraternistas.count() + juventude.codigos_cadastro.count() >= \
       juventude.limite_confraternistas:
        messages.add_message(request, messages.ERROR, 
            "O limite de confraternistas da sua Juventude Espírita foi atingido.\n"
            "Caso queira cadastrar outros confraternistas, entre em contato com a coordenação geral.")
    else:
        codigo = models.CodigoCadastro(juventude=juventude, coordenador=False)
        codigo.save()
        messages.add_message(request, messages.INFO, "Código criado com sucesso!")

    return HttpResponseRedirect("/coordenador/novo_confraternista")



@user_is_coordenador
def listar_confraternistas(request):
    confraternistas = models.Confraternista.objects.filter(juventude=request.user.coordenador.juventude)

    return render_to_response("coordenador/listar_confraternistas.html", 
                              RequestContext(request, {"confraternistas": confraternistas,
                                                       "juventude": request.user.coordenador.juventude}))



user_is_coordenador
def autorizar_confraternista(request):
    confraternista = models.Confraternista.objects.get(id=request.GET.get("id"))

    if not confraternista or confraternista.juventude != request.user.coordenador.juventude:
        return HttpResponseForbidden()

    confraternista.autorizado = True
    confraternista.save()

    messages.add_message(request, messages.INFO, "Confraternista autorizado!")
    return HttpResponseRedirect("/coordenador/listar_confraternistas")



def novo_usuario(request):

    form = (forms.NovoUsuario() 
            if request.method != 'POST' 
            else forms.NovoUsuario(request.POST))

    if form.is_bound and form.is_valid():
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
            else:
                conf = models.Confraternista()
                conf.usuario = usuario
                conf.juventude = codigo.juventude
                conf.save()

            codigo.delete()

            messages.add_message(request, messages.INFO, u"Seu cadastro foi realizado! Você pode fazer login agora.")
            return HttpResponseRedirect("/")
    
    return render_to_response("cadastro.html", 
            RequestContext(request, {"form": form}))



def editar_dados(request):

    #id do confraternista, para o caso de o coordenador estar editando os dados
    conf_id = None if request.method != 'GET' else request.GET.get('id')

    is_coordenador = hasattr(request.user, 'coordenador')
    is_confraternista = hasattr(request.user, 'confraternista')

    conf = None

    if is_coordenador:
        if conf_id:
            confraternista = models.Confraternista.objects.get(id=int(conf_id))
        else:
            confraternista = request.user.confraternista
    else:
        confraternista = request.user.confraternista

    form = (forms.InscricaoConfraternista(instance=confraternista)
            if request.method != 'POST' 
            else forms.InscricaoConfraternista(request.POST))

    if form.is_valid():
        
        #if not (is_coordenador and request.POST['conf_id']):
        #    conf = request.user.confraternista
        #else:
        #    conf = Confraternista.get(int(request.POST['conf_id']))

        for attr in ["nome_cracha", "sexo", "data_nascimento",
                     "ano_ingresso_mocidade", "comebhs_anteriores",
                     "logradouro", "bairro", "cidade",
                     "telefone", "contato_urgencia", "parentesco_contato_urgencia",
                     "telefone_contato_urgencia", "telefone2_contato_urgencia",
                     "dieta_especial", "uso_medicamento", "alergia",
                     "voluntario_manutencao", "tamanho_camisa"]:
            setattr(confraternista, attr, form.cleaned_data.get(attr) or None)

        if request.POST['r_comprar_camisa'] == '0':
            confraternista.tamanho_camisa = None

        confraternista.save()

        messages.add_message(request, messages.INFO, "Dados de inscrição salvos com sucesso!")

        return HttpResponseRedirect("/")

    return render_to_response("confraternista/editar_dados.html",
                              RequestContext(request, 
                                             {"form": form,
                                              "conf_id": conf_id,
                                              "juventude": request.user.confraternista.juventude 
                                                           if is_confraternista
                                                           else request.user.coordenador.juventude}))


def imprimir_autorizacao_pais(request):
    if request.GET.get("id"):
        nome = models.Confraternista.objects.get(id=int(request.GET.get("id"))).usuario.get_full_name()
    else:
        nome = request.user.get_full_name()

    return render_to_response("confraternista/autorizacao.html", 
                              RequestContext(request, {"nome": nome}))