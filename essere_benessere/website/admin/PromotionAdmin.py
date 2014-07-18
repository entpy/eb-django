# -*- coding: utf-8 -*-

from website.models import Account, Promotion, Campaign
from website.forms import *
from django.contrib import admin, messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
from datetime import datetime
import logging

# Get an instance of a logger
logger = logging.getLogger('django.request')

class PromotionAdmin(admin.ModelAdmin):

        # fileds in add/modify form
        fields = ('name', 'description', 'promo_image', 'expiring_date')

        # table list fields
        list_display = ('name', 'expiring_date')

        # showing only valid promotion
        def queryset(self, request):
                qs = super(PromotionAdmin, self).queryset(request)
                return qs.filter(expiring_date__gte=datetime.now().date()).filter(promo_type=Promotion.PROMOTION_TYPE_FRONTEND["key"])

        def save_model(self, request, obj, form, change):
                """
                Overriding of "save_model" to generate a campaign code after
                promotion saving (only if not exists yet)
                """

                campaign_obj = Campaign()

                # setting promo type to frontend post
                obj.promo_type = Promotion.PROMOTION_TYPE_FRONTEND["key"]
                obj.save()
                id_promotion = obj.id_promotion

                # generating a campaign code, if not exist yet
                campaign_obj.add_frontend_post_campaign(id_promotion=id_promotion)
