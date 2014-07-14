# -*- coding: utf-8 -*-

from website.models import Account, Promotion, Campaign
from website.forms import *
from django.contrib import admin, messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
import logging

# Get an instance of a logger
logger = logging.getLogger('django.request')

class PromotionAdmin(admin.ModelAdmin):

        # fileds in add/modify form
        fields = ('name', 'description', 'promo_image', 'expiring_date')

        # table list fields
        list_display = ('name', 'expiring_date')

        def save_model(self, request, obj, form, change):
                # setting promo type to frontend post
                obj.promo_type = Promotion.PROMOTION_TYPE_FRONTEND["key"]
                obj.save()
