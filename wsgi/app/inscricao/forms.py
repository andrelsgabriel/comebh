#-*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
import models

class EditarJuventude(forms.ModelForm):

    contato = forms.CharField(widget=forms.Textarea())

    nome_casa_espirita = forms.CharField(widget=forms.TextInput(attrs={"size":40}),
                                         label="Nome da Casa Espírita")

    logradouro = forms.CharField()
    bairro = forms.CharField()
    cidade = forms.CharField()

    class Meta:
        model = models.JuventudeEspirita
        exclude = ('limite_confraternistas',)



class ConviteConfraternista(forms.Form):
    nome = forms.CharField()
    email = forms.EmailField()



class ConviteCoordenador(forms.Form):
    nome = forms.CharField()
    email = forms.EmailField()
    juventude = forms.ModelChoiceField(queryset=models.JuventudeEspirita.objects.all(), empty_label=None)



class NovoUsuario(forms.Form):
    nome = forms.CharField(label="Nome completo")
    email = forms.EmailField(label="Email")

    login = forms.CharField()
    senha = forms.CharField(widget=forms.PasswordInput())
    senha_confirmacao = forms.CharField(label=u"Confirmação da Senha", widget=forms.PasswordInput())
    codigo = forms.IntegerField(widget=forms.HiddenInput())

    def clean(self):
        if 'login' in self.cleaned_data and \
            User.objects.filter(username=self.cleaned_data['login']).count() != 0:
            if User.objects.get(username=self.cleaned_data["login"]).email  != self.cleaned_data["email"]:
                self.errors['login'] = (self.errors.get('login') or []) + [u"Este login já está sendo usado."]

        if 'codigo' in self.cleaned_data and \
            models.CodigoCadastro.objects.filter(codigo=self.cleaned_data['codigo']).count() == 0:
            self.errors['codigo'] = (self.errors.get('codigo') or []) + [u"Código de cadastro inválido."]

        if 'nome' in self.cleaned_data and \
            len(self.cleaned_data['nome'].split(" ")) == 1:
            self.errors['nome'] = (self.errors.get('nome') or []) + [u"Digite seu nome completo, não apenas o primeiro nome."]

        return self.cleaned_data

    def clean_senha_confirmacao(self):
        if self.cleaned_data['senha_confirmacao'] != self.cleaned_data['senha']:
            self.errors['senha_confirmacao'] = ((self.errors.get('senha_confirmacao') or []) +
                                                [u"As senhas digitadas são diferentes."])

        return self.cleaned_data['senha_confirmacao']



class AlterarUsuario(forms.Form):
    nome = forms.CharField(label="Nome completo")
    email = forms.EmailField()
    senha = forms.CharField(widget=forms.PasswordInput(), required=False)
    senha_confirmacao = forms.CharField(label=u"Confirmação da senha", widget=forms.PasswordInput(), required=False)

    def clean_senha_confirmacao(self):
        if self.cleaned_data['senha_confirmacao'] != self.cleaned_data['senha']:
            self.errors['senha_confirmacao'] = ((self.errors.get('senha_confirmacao') or []) +
                                                [u"As senhas digitadas são diferentes."])

        return self.cleaned_data['senha_confirmacao']



class InscricaoConfraternista(forms.ModelForm):

    nome_cracha = forms.CharField()
    sexo = forms.ChoiceField(choices=(("M", "Masculino"), ("F", "Feminino")))
    data_nascimento = forms.DateField()
    ano_ingresso_mocidade = forms.IntegerField()
    identidade = forms.CharField()
    comebhs_anteriores = forms.CharField(required=False)

    logradouro = forms.CharField()
    bairro = forms.CharField()
    cidade = forms.CharField()

    telefone = forms.CharField()
    contato_urgencia = forms.CharField()
    parentesco_contato_urgencia = forms.CharField()
    telefone_contato_urgencia = forms.CharField()
    telefone2_contato_urgencia = forms.CharField()

    dieta_especial = forms.CharField(required=False, widget=forms.Textarea())
    uso_medicamento = forms.CharField(required=False, widget=forms.Textarea())
    alergia = forms.CharField(required=False, widget=forms.Textarea())

    voluntario_manutencao = forms.BooleanField(required=False)
    tamanho_camisa = forms.ChoiceField(required=False, choices=[("", "---")] + list(models.Confraternista.TAMANHOS_CAMISA))

    class Meta:
        model = models.Confraternista
        exclude = ("usuario", "juventude", "autorizado", "pagamento_inscricao", "comebh")



class DadosUsuario(forms.Form):
    nome = forms.CharField(label="Nome completo")
    email = forms.EmailField(label="Email")

    senha = forms.CharField(label=u"Nova senha", widget=forms.PasswordInput())
    senha_confirmacao = forms.CharField(label=u"Confirmação da Senha", widget=forms.PasswordInput())


class Comebh(forms.ModelForm):
    class Meta:
        model = models.Comebh
