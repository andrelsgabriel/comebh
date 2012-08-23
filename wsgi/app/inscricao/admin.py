from django.contrib import admin
from models import *

for m in [JuventudeEspirita,
		  Coordenador,
		  Confraternista,
		  Pagamento,
		  CodigoCadastro]:
	admin.site.register(m)