import os
from django.conf.urls import patterns, include, url
from inscricao import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

js_folder = os.path.join(os.path.join(os.path.dirname(__file__), "js"))
css_folder = os.path.join(os.path.join(os.path.dirname(__file__), "css"))
images_folder = os.path.join(os.path.join(os.path.dirname(__file__), "images"))

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'comebh.views.home', name='home'),
    # url(r'^comebh/', include('comebh.foo.urls')),
    url(r'^$', 'inscricao.views.principal'),
    url(r'^sair/$', 'inscricao.views.sair'),
    url(r'^coordenador/editar_juventude', views.editar_juventude),
    url(r'^coordenador/salvar_juventude', views.salvar_juventude),
    url(r'^coordenador/novo_confraternista', views.novo_confraternista),
    url(r'^coordenador/listar_confraternistas', views.listar_confraternistas),
    url(r'^coordenador/criar_codigo_cadastro', views.criar_codigo_cadastro),
    url(r'^coordenador/autorizar', views.autorizar_confraternista),
    url(r'^cadastro/$', views.novo_usuario),
    url(r'^confraternista/editar_dados', views.editar_dados),
    url(r'^confraternista/imprimir_autorizacao_pais', views.imprimir_autorizacao_pais),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^js/(?P<path>.*)', 'django.views.static.serve', {'document_root': js_folder}),
    url(r'^css/(?P<path>.*)', 'django.views.static.serve', {'document_root': css_folder}),
    url(r'^images/(?P<path>.*)', 'django.views.static.serve', {'document_root': images_folder})
)
