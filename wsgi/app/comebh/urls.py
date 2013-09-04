import os
from django.conf.urls import patterns, include, url
from inscricao import views, pagseguro

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'comebh.views.home', name='home'),
    # url(r'^comebh/', include('comebh.foo.urls')),
    url(r'^$', 'inscricao.views.principal'),
    url(r'^sair/$', 'inscricao.views.sair'),
    url(r'^editar_usuario/$', views.editar_usuario),

    url(r'^administrador/convites_coordenador', views.ver_convites_coordenador),
    url(r'^administrador/convidar_coordenador', views.convidar_coordenador),
    url(r'^administrador/reenviar_convite_coordenador', views.reenviar_convite_coordenador),
    url(r'^administrador/desfazer_convite_coordenador', views.desfazer_convite_coordenador),
    url(r'^administrador/editar_comebh', views.editar_comebh),
    url(r'^administrador/salvar_comebh', views.salvar_comebh),
    url(r'^administrador/criar_comebh', views.criar_comebh),

    url(r'^coordenador/editar_juventude', views.editar_juventude),
    url(r'^coordenador/salvar_juventude', views.salvar_juventude),
    url(r'^coordenador/novo_confraternista', views.novo_confraternista),
    url(r'^coordenador/listar_confraternistas', views.listar_confraternistas),
    url(r'^coordenador/criar_codigo_cadastro', views.criar_codigo_cadastro),
    url(r'^coordenador/desfazer_convite', views.desfazer_convite),
    url(r'^coordenador/autorizar', views.autorizar_confraternista),
    url(r'^coordenador/pagarInscricao', views.adicionar_inscricao_pagamento),
    url(r'^coordenador/limparInscricoes', views.limpar_inscricoes),
    url(r'^coordenador/pagarInscricoes', views.redirecionar_pagamento),
    url(r'^coordenador/autorizacao_casa_espirita', views.imprimir_autorizacao_casa_espirita),
    url(r'^coordenador/reenviar_email_convite', views.reenviar_email_convite),
    url(r'^recuperar_senha', views.recuperar_senha),

    url(r'^cadastro/', views.novo_usuario),

    url(r'^confraternista/editar_dados', views.editar_dados),
    url(r'^confraternista/realizar_pagamento', views.confraternista_realizar_pagamento),
    url(r'^confraternista/imprimir_autorizacao_pais', views.imprimir_autorizacao_pais),

    url(r'^notificacao/?', pagseguro.processar_notificacao),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login'),
)
