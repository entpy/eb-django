# -*- coding: utf-8 -*-

from website.models import Account, Promotion, Campaign
from .AccountAdmin import *
from .PromotionAdmin import *
from django.contrib import admin, messages

# registering models to admin interface
admin.site.register(Account, AccountAdmin)
admin.site.register(Promotion, PromotionAdmin)
