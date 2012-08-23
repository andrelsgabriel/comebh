#-*- coding: utf-8 -*-

import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class JuventudeEspirita(models.Model):
    nome = models.CharField('nome', max_length=80, unique=True)
    contato = models.TextField('contato', blank=True)

    nome_casa_espirita = models.CharField('nome da Casa Espírita', max_length=80, unique=True, blank=True)

    logradouro = models.CharField('logradouro', max_length=255, blank=True)
    bairro = models.CharField('bairro', max_length=255, blank=True)
    cidade = models.CharField('cidade', max_length=255, blank=True)

    limite_confraternistas = models.PositiveIntegerField('limite de confraternistas')

    def __unicode__(self):
        return self.nome


    def isCoordenador(self, usuario):
        return usuario.coordenador and usuario.coordenador.juventude == self



class Coordenador(models.Model):
    usuario = models.OneToOneField(User, related_name="coordenador")
    juventude = models.ForeignKey(JuventudeEspirita, related_name="coordenadores")

    def __unicode__(self):
        return u"{.first_name} (coordena a juventude {.nome})".format(self.usuario, self.juventude)



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
            (7, u"Cancelado")
        )

    transacao_pagseguro = models.CharField(max_length=255, unique=True, null=True)
    data = models.DateField(auto_now_add=True)
    valor_bruto = models.DecimalField(max_digits=10, decimal_places=2)
    valor_liquido = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS_PAGAMENTO, default=0)

    def get_estado_str(self):
        return Pagamento.ESTADOS_PAGAMENTO[self.estado][1]




class Confraternista(models.Model):

    TAMANHOS_CAMISA = (("P", u"Pequena"), 
                       ("M", u"Média"),
                       ("G", u"Grande"))

    usuario = models.OneToOneField(User)
    
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
    contato_urgencia = models.CharField(max_length=255, null=True, blank=True)
    parentesco_contato_urgencia = models.CharField(max_length=255, null=True, blank=True)
    telefone_contato_urgencia = models.CharField(max_length=255, null=True, blank=True)
    telefone2_contato_urgencia = models.CharField(max_length=255, null=True, blank=True)

    ano_ingresso_mocidade = models.PositiveIntegerField(null=True, blank=True)
    comebhs_anteriores = models.CommaSeparatedIntegerField(max_length=255, null=True, blank=True)

    dieta_especial = models.TextField(null=True, blank=True)
    uso_medicamento = models.TextField(null=True, blank=True)
    alergia = models.TextField(null=True, blank=True)

    tamanho_camisa = models.CharField(null=True, blank=True, max_length=1, 
        choices=TAMANHOS_CAMISA)

    pagamento_inscricao = models.ForeignKey(Pagamento, null=True, blank=True, related_name="confraternistas")

    def __unicode__(self):
        return self.usuario.get_full_name() + " - " + self.juventude.nome


    def precisa_autorizacao_pais(self):
        return self.data_nascimento and \
            self.data_nascimento > datetime.date(settings.DATA_COMEBH.year - 18,
                                                 settings.DATA_COMEBH.month,
                                                 settings.DATA_COMEBH.day)



class CodigoCadastro(models.Model):
    codigo = models.IntegerField(unique=True)
    juventude = models.ForeignKey(JuventudeEspirita, related_name="codigos_cadastro")
    coordenador = models.BooleanField()


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
