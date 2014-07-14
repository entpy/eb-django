# -*- coding: utf-8 -*-

from website.models import Account, Promotion, Campaign
from .AccountAdmin import *
from .PromotionAdmin import *
from django.contrib import admin, messages

# registering models to admin interface
admin.site.register(Account, AccountAdmin)
admin.site.register(Promotion, PromotionAdmin)

# TODO list
"""
- Sovrascrivere il delete delle promozioni eliminando anche le relative righe in campagne
- Sovrascrivere il metodo save dell'immagine per farne prima il resize
- Aggiungere ulteriori link nella index dell'admin
- Al salvataggio del form di mofica/inserimento promozione generare, se non
esiste, anche un codice della campagna.
"""
