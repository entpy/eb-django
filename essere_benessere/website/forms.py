# -*- coding: utf-8 -*-

from website.models import Account, Promotion, Campaign
from django import forms
from django.contrib.admin import widgets 

class PromotionForm(forms.ModelForm):
        """
        Form to add/edit a promotion from create campaign steps
        NB: this in not the django add/change default form for Promotion app
        """

        # promo_image = forms.ImageField(upload_to="/tmp/")

        class Meta:
                widgets = {'expiring_date': widgets.AdminDateWidget()}
                model = Promotion
                fields = ['name', 'description', 'promo_image', 'expiring_date']

class BirthdayPromotionForm(forms.ModelForm):
        """
        Form to add/change or remove a birthday promotion
        """

        # promo_image = forms.ImageField(upload_to="/tmp/")

        class Meta:
                model = Promotion
                fields = ['name', 'description', 'promo_image']

class ValidateCodeForm(forms.Form):
        """
        Form to validate a coupon code, this form is not related with any object
        """

        promo_code = forms.CharField(max_length=10, required=True)
