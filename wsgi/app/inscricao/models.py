#-*- coding: utf-8 -*-

import datetime
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import admin

class JuventudeEspirita(models.Model):
    nome = models.CharField('nome', max_length=80, unique=True)
    contato = models.TextField('contato', blank=True)

    nome_casa_espirita = models.CharField('nome da Casa Espírita', max_length=80, unique=True, blank=True)

    logradouro = models.CharField('logradouro', max_length=255, blank=True)
    bairro = models.CharField('bairro', max_length=255, blank=True)
    cidade = models.CharField('cidade', max_length=255, blank=True)

    limite_confraternistas = models.PositiveIntegerField('limite de confraternistas (fichas)')

    def clean(self):
        if self.limite_confraternistas < self.confraternistas.count():
            raise ValidationError(u"O limite de confraternistas da Juventude Espírita deve ser maior que o número de confraternistas cadastrados.")

    def __unicode__(self):
        return self.nome


    def isCoordenador(self, usuario):
        return usuario.coordenador and usuario.coordenador.juventude == self

    inscricoes_disponiveis = property(lambda self: self.limite_confraternistas - self.confraternistas.count())
    inscricoes_utilizadas = property(lambda self: self.confraternistas.count())

    class Meta:
        verbose_name = "Juventude Espírita"
        verbose_name_plural = "Juventudes Espíritas"

    class Admin(admin.ModelAdmin):
        list_display = ("nome", "nome_casa_espirita", "cidade", "limite_confraternistas", "inscricoes_utilizadas", "inscricoes_disponiveis")
        search_fields = ("nome", "bairro", "cidade")
        ordering = ("nome",)


class Comebh(models.Model):

    valor_inscricao = models.DecimalField(max_digits=10, decimal_places=2)
    valor_camisa = models.DecimalField(max_digits=10, decimal_places=2)

    data_evento = models.DateField()
    limite_inscricoes = models.IntegerField()

    data_limite_inscricoes = models.DateField(u"Data limite para inscrições")
    idade_minima = models.IntegerField(u"Idade mínima para participação (anos)")

    class Meta:
        verbose_name = u"Configuração da COMEBH"
        verbose_name_plural = "Configurações Gerais da COMEBH"

    class Admin(admin.ModelAdmin):
        list_display = ("data", "valor_inscricao", "valor_camisa", "limite_inscricoes")

    @staticmethod
    def comebh_vigente():
        if Comebh.objects.count() == 0:
            return None
        return Comebh.objects.order_by("-data_evento")[0]

    def ano(self):
        return self.data_evento.year

    def __unicode__(self):
        return "COMEBH {0}".format(self.ano())


class Coordenador(models.Model):
    usuario = models.ForeignKey(User, related_name="coordenadores")
    juventude = models.ForeignKey(JuventudeEspirita, related_name="coordenadores", verbose_name=u"Juventude Espírita")
    comebh = models.ForeignKey(Comebh, related_name="coordenadores", null=True)

    nome = property(lambda self: self.usuario.get_full_name())

    @staticmethod
    def do_usuario(usuario):
        if hasattr(usuario, 'coordenadores') and usuario.coordenadores.count():
            c = usuario.coordenadores.order_by("-comebh__data_evento")[0]
            if c.comebh == Comebh.comebh_vigente():
                return c

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Coordenadores"

    class Admin(admin.ModelAdmin):
        class FiltroPorAno(admin.SimpleListFilter):
            title = "Por ano"
            parameter_name = "comebh"

            def lookups(*args):
                return tuple((str(comebh.ano()), comebh.ano()) for comebh in Comebh.objects.all())

            def queryset(self, request, queryset):
                if not self.value():
                    return queryset
                return queryset.filter(comebh__data_evento__year=self.value())

        list_display = ("nome", "juventude")
        list_filter = ("juventude", FiltroPorAno)
        search_fields = ("nome", "juventude")



        #ordering = ("nome",)



class Pagamento(models.Model):

    #possíveis estados de uma transação do PagSeguro
    #pagseguro.uol.com.br/v2/guia-de-integracao/consulta-de-transacoes-por-codigo.html
    ESTADOS_PAGAMENTO = (
            (0, u"Desconhecido"),
            (1, u"PagSeguro Aguardando pagamento"),
            (2, u"Em análise pelo PagSeguro"),
            (3, u"Pago"),
            (4, u"Pago e liberado para retirada"),
            (5, u"Em disputa"),
            (6, u"Devolvido"),
            (7, u"Cancelado"),
            (8, u"Isento")
        )

    transacao_pagseguro = models.CharField(max_length=255, unique=True, null=True)
    data = models.DateField(auto_now_add=True)
    valor_bruto = models.DecimalField(max_digits=10, decimal_places=2)
    valor_liquido = models.DecimalField(u"valor líquido (com descontos)", max_digits=10, decimal_places=2, blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS_PAGAMENTO, default=0)

    def __unicode__(self):
        return self.get_estado_str()

    def get_estado_str(self):
        return Pagamento.ESTADOS_PAGAMENTO[self.estado][1]

    pago = property(lambda self: self.estado == 3 or self.estado == 4)

    class Admin(admin.ModelAdmin):
        list_display = ("data", "valor_bruto", "valor_liquido", "estado")
        list_filter = ("estado",)



class Confraternista(models.Model):

    TAMANHOS_CAMISA = (("P", u"Pequena"),
                       ("M", u"Média"),
                       ("G", u"Grande"))

    usuario = models.ForeignKey(User, related_name="confraternistas")

    identidade = models.CharField(max_length=255, blank=True)
    nome_cracha = models.CharField(max_length=255, blank=True)
    juventude = models.ForeignKey(JuventudeEspirita, related_name="confraternistas")
    data_nascimento = models.DateField(blank=True, null=True)
    voluntario_manutencao = models.BooleanField(default=False)
    autorizado = models.BooleanField(default=False)
    sexo = models.CharField(max_length=1, choices= (("M", "Masculino"), ("F", "Feminino")), null=True, blank=True)

    logradouro = models.CharField(max_length=255, null=True, blank=True)
    bairro = models.CharField(max_length=255, null=True, blank=True)
    cidade = models.CharField(max_length=255, null=True, blank=True)

    telefone = models.CharField(max_length=20, null=True, blank=True)
    contato_urgencia = models.CharField(u"contato (para urgência)", max_length=255, null=True, blank=True)
    parentesco_contato_urgencia = models.CharField(u"parentesco do contato de urgência", max_length=255, null=True, blank=True)
    telefone_contato_urgencia = models.CharField(u"telefone do contato de urgência", max_length=255, null=True, blank=True)
    telefone2_contato_urgencia = models.CharField(u"outro telefone de urgência", max_length=255, null=True, blank=True)

    ano_ingresso_mocidade = models.PositiveIntegerField(u"ano de ingresso na Juventude Espírita", null=True, blank=True)
    comebhs_anteriores = models.CommaSeparatedIntegerField("COMEBHS anteriores", max_length=255, null=True, blank=True)

    dieta_especial = models.TextField(null=True, blank=True)
    uso_medicamento = models.TextField(u"Uso controlado de medicamento", null=True, blank=True)
    alergia = models.TextField(null=True, blank=True)

    tamanho_camisa = models.CharField(u"tamanho da camisa", null=True, blank=True, max_length=1,
        choices=TAMANHOS_CAMISA)

    pagamento_inscricao = models.ForeignKey(Pagamento, null=True, blank=True, related_name="confraternistas")

    comebh = models.ForeignKey(Comebh, related_name="confraternistas", null=True)


    @staticmethod
    def do_usuario(usuario):
        if hasattr(usuario, 'confraternistas') and usuario.confraternistas.count():
            c = usuario.confraternistas.order_by("-comebh__data_evento")[0]
            if c.comebh == Comebh.comebh_vigente():
                return c


    def __unicode__(self):
        return self.usuario.get_full_name() + " (" + self.juventude.nome + ")"


    def precisa_autorizacao_pais(self):
        c = Comebh.comebh_vigente()
        return self.data_nascimento and \
            self.data_nascimento > datetime.date(c.data_evento.year - 18,
                                                 c.data_evento.month,
                                                 c.data_evento.day)

    def valor_inscricao(self):
        c = Comebh.comebh_vigente()
        return c.valor_inscricao + (c.valor_camisa if self.tamanho_camisa else 0)


    nome = property(lambda self: self.usuario.get_full_name())
    preco_inscricao = property(lambda self: "R${0:.2f}".format(self.valor_inscricao()))
    tem_restricoes_alimentares = property(lambda self: u"Sim" if self.dieta_especial else u"Não")
    deseja_ajudar_manutencao = property(lambda self: u"Sim" if self.voluntario_manutencao else u"Não")

    class Admin(admin.ModelAdmin):

        class FiltroPorAno(admin.SimpleListFilter):
            title = "Por ano"
            parameter_name = "comebh"

            def lookups(*args):
                return tuple((str(comebh.ano()), comebh.ano()) for comebh in Comebh.objects.all())

            def queryset(self, request, queryset):
                if not self.value():
                    return queryset
                return queryset.filter(comebh__data_evento__year=self.value())


        class FiltroPorIdade(admin.SimpleListFilter):
            title = "Por idade"
            parameter_name = "idade"

            def lookups(*args):
                return (("M", "Maiores de idade"),
                        ("m", "Menores de idade"))

            def queryset(self, request, queryset):
                c = Comebh.comebh_vigente()

                data_minima = datetime.date(c.data_evento.year - 18,
                                            c.data_evento.month,
                                            c.data_evento.day)

                if self.value() == "m":
                    return queryset.filter(data_nascimento__gt=data_minima)
                elif self.value() == "M":
                    return queryset.filter(data_nascimento__lte=data_minima)

        class FiltroPorEstadoPagamento(admin.SimpleListFilter):
            title = "estado de pagamento"
            parameter_name = "estado_pagamento"

            def lookups(*args):
                return Pagamento.ESTADOS_PAGAMENTO

            def queryset(self, request, queryset):
                if self.value():
                    return queryset.filter(pagamento_inscricao__in=Pagamento.objects.filter(estado=self.value()))


        class FiltroPorRestricaoAlimentar(admin.SimpleListFilter):
            title = u"restrição alimentar"
            parameter_name = "restricao_alimentar"

            def lookups(*args):
                return (("S", u"Possui"),
                        ("N", u"Não possui"))

            def queryset(self, request, queryset):
                if self.value():
                    if self.value() == 'S':
                        return queryset.filter(Q(dieta_especial__isnull=False) & ~Q(dieta_especial=""))
                    else:
                        return queryset.filter(Q(dieta_especial__isnull=True) | Q(dieta_especial=""))


        list_display = ("nome", "juventude", "data_nascimento", "autorizado", "pagamento_inscricao",
                        "preco_inscricao", "tamanho_camisa", "tem_restricoes_alimentares")
        list_filter = ("juventude", "autorizado", "voluntario_manutencao", "tamanho_camisa",
                        FiltroPorAno, FiltroPorIdade, FiltroPorEstadoPagamento, FiltroPorRestricaoAlimentar)
        search_fields = ("juventude", "data_nascimento")
        ordering = ("juventude",)



class CodigoCadastro(models.Model):
    codigo = models.IntegerField(unique=True)
    juventude = models.ForeignKey(JuventudeEspirita, related_name="codigos_cadastro")
    coordenador = models.BooleanField()
    confraternista = models.BooleanField(default=True)
    nome = models.CharField(max_length=255)
    email = models.EmailField()

    def save(self, *args, **kwargs):
        if self.codigo is None:
            import random

            valido = False

            while not valido:
                self.codigo = random.randint(10**5, 10**6)
                valido = CodigoCadastro.objects.filter(codigo=self.codigo).count() == 0

        models.Model.save(self, *args, **kwargs)


    def __unicode__(self):
        return unicode(self.codigo)

