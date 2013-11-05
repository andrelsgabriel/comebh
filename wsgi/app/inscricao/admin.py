import datetime
from django.contrib import admin
from django.conf import settings
from models import *



for m in [JuventudeEspirita,
          Coordenador,
          Confraternista,
          Pagamento,
          Comebh]:
    if hasattr(m, 'Admin'):
        admin.site.register(m, m.Admin)
    else:
        admin.site.register(m)
