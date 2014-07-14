# -*- coding: utf-8 -*-

from website.models import Account, Promotion, Campaign
from website.forms import *
from django.conf.urls import patterns
from django.contrib import admin, messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
import logging

# Get an instance of a logger
logger = logging.getLogger('django.request')

class AccountAdmin(admin.ModelAdmin):

        # fileds in add/modify form
        fields = (('first_name', 'last_name'), 'email', 'mobile_phone', 'birthday_date', ('receive_promotions', 'loyal_customer'))

        # table list fields
        list_display = ('email', 'mobile_phone', 'first_name', 'last_name')

        # URLs overwriting to add new admin views (with auth check and without cache)
        def get_urls(self):
                urls = super(AccountAdmin, self).get_urls()
                my_urls = patterns('',
                        (r'^campaigns/step1/(?P<new_campaign>\d+)?$', self.admin_site.admin_view(self.create_promotion)),
                        (r'^campaigns/step2$', self.admin_site.admin_view(self.select_recipients)),
                        (r'^campaigns/step3/(?P<id_promotion>\d+)?$', self.admin_site.admin_view(self.campaign_review)),
                        (r'^code_validator$', self.admin_site.admin_view(self.code_validator)),
                        (r'^birthday_promo$', self.admin_site.admin_view(self.set_birthday_promo)),
                )

                # return custom URLs with default URLs
                return my_urls + urls

        def set_birthday_promo(self, request):
                """
                Function to create/edit or remove a birthday promo
                """

                promotion_obj = Promotion()

                if request.method == 'POST':

                        # checking if birthday promo must be deleted
                        if request.POST.get("delete"):
                                promotion_obj.delete_birthday_promotion()
                                messages.add_message(request, messages.SUCCESS, 'Promozione compleanno eliminata correttamente')
                                return HttpResponseRedirect('/admin/website/account/birthday_promo') # Redirect after POST

                        form = BirthdayPromotionForm(request.POST, request.FILES, instance=promotion_obj.get_birthday_promotion_instance())

                        if form.is_valid():
                                # saving birthday promo form (creting only instance without saving)
                                birthday_promo_obj = form.save(commit=False)
                                # setting promo type to birthday_promo before saving
                                birthday_promo_obj.promo_type = Promotion.PROMOTION_TYPE_BIRTHDAY["key"]
                                # saving instance into db
                                birthday_promo_obj.save()

                                messages.add_message(request, messages.SUCCESS, 'Promozione compleanno modificata correttamente')
                                return HttpResponseRedirect('/admin/website/account/birthday_promo') # Redirect after POST
                else:
                        # empty or change birthday promo form
                        form = BirthdayPromotionForm(instance=promotion_obj.get_birthday_promotion_instance())

                context = {
                        'adminform' : form,
			'title': "Promozione compleanno",
			'opts': self.model._meta,
			'app_label': self.model._meta.app_label,
			'has_change_permission': True,
			'has_file_field' : True,
                }

                return render(request, 'admin/custom_view/birthday_promo.html', context)

        def code_validator(self, request):
                """
                Function to validate a coupon code
                """

                can_redeem = False
                promotion_details = {}

                if request.method == 'POST':
                        form = ValidateCodeForm(request.POST)

                        # cancel operation
                        if (request.POST.get("cancel", "")):
                                messages.add_message(request, messages.WARNING, 'Operazione annullata.')
                                return HttpResponseRedirect('/admin/website/account/code_validator') # Redirect after POST

                        if form.is_valid():
                                post_code = request.POST.get("promo_code")

                                # retrieving promotion details
                                campaign_obj = Campaign()

                                # checking if code exists
                                if (not campaign_obj.check_code_validity(code=post_code, validity_check="exists")):
                                        messages.add_message(request, messages.ERROR, 'Codice promozionale non esistente.')
                                        return HttpResponseRedirect('/admin/website/account/code_validator') # Redirect after POST

                                # checking if code is not already validated
                                if (not campaign_obj.check_code_validity(code=post_code, validity_check="not_used")):
                                        messages.add_message(request, messages.ERROR, 'Codice promozionale già validato.')
                                        return HttpResponseRedirect('/admin/website/account/code_validator') # Redirect after POST

                                # checking if campaign is not expired
                                if (not campaign_obj.check_code_validity(code=post_code, validity_check="not_expired")):
                                        messages.add_message(request, messages.ERROR, 'Codice promozionale scaduto.')
                                        return HttpResponseRedirect('/admin/website/account/code_validator') # Redirect after POST

                                # user can redeem the code
                                can_redeem = True

                                # show promotion details
                                promotion_details = campaign_obj.get_campaign_details(campaign_code=post_code)

                                if (request.POST.get("redeem_code", "")):
                                        # redeem code and redirect to success page
                                        campaign_obj.redeem_code(post_code)
                                        messages.add_message(request, messages.SUCCESS, 'Codice promozionale validato!')
                                        return HttpResponseRedirect('/admin/website/account/code_validator') # Redirect after POST
                else:
                        form = ValidateCodeForm() # An unbound form

                context = {
                        'form' : form,
                        'redeem_code' : can_redeem,
                        'promotion_details' : promotion_details,
                        'title': "Validatore di codici",
                        'opts': self.model._meta,
                        'app_label': self.model._meta.app_label,
                }

                return render(request, 'admin/custom_view/code_validator.html', context)

        # STEP 1
        def create_promotion(self, request, new_campaign=False):

                # retrieving id promotion from GET (if exists and saving into session)
                if (new_campaign):
                        request.session['promotion_id'] = None

                # 1: get add promotion form
                try:
                        # get promo id from session
                        promotion_obj = None
                        promotion_obj = Promotion.objects.get(id_promotion=request.session['promotion_id'])
                except (KeyError, Promotion.DoesNotExist):
                        # object doesn't exists
                        pass

                if (request.method == 'POST'):
                        formset = PromotionForm(request.POST, request.FILES, instance=promotion_obj)
                        if formset.is_valid():
                                promo = formset.save()

                                # saving created promotion id into session
                                # logger.debug("Promo id creata: " + str(promo.id_promotion))
                                request.session['promotion_id'] = promo.id_promotion

                                # redirect to campaigns/step2
                                return HttpResponseRedirect('/admin/website/account/campaigns/step2') # Redirect after POST
                else:
                        # retrieving a model form starting from primary model key
                        formset = PromotionForm(instance=promotion_obj)

		logger.debug("selected_contacts_list: " + str(formset))
                # creating template context
                context = {
                        'adminform' : formset,
			'title': "Crea la promozione",
			'opts': self.model._meta,
			'app_label': self.model._meta.app_label,
                }

                return render(request, 'admin/custom_view/campaigns/step1.html', context)

        # STEP 2
        def select_recipients(self, request):
                """
                Send campaign wizard view, a custom admin view to enable
                sending promotion to a customer list
                """

                # a campaign must exists before enter here
                if (request.session['promotion_id'] is None):
                        return HttpResponseRedirect('/admin/website/account/campaigns/step1')

                contact_list = Account.objects.all()
                campaign_obj = Campaign()
                paginator = Paginator(contact_list, 5)
		working_id_promotion = request.session['promotion_id']

		# retrieving new page number
                if (request.POST.get('next', '')):
                        page = request.POST.get('next_page')
                else:
                        page = request.POST.get('previously_page')

		# retrieving old page number
                old_viewed_page = request.POST.get('current_page')

                """1""" # set/unset campaign senders: saving checked and delete unchecked checkbox from form into db/session if POST exists
                if(request.POST.get("select_senders_form_sent", "") and request.POST.get("current_page", "")):
                        selected_contacts = request.POST.getlist("contacts[]")

                        # retrieving checked list from current view (only checkbox that are shown from paginator current view)
                        senders_dictionary = campaign_obj.get_checkbox_dictionary(paginator.page(old_viewed_page), selected_contacts, "id_account")

                        # saving or removing checked/unchecked checkbox from db
                        campaign_obj.set_campaign_user(senders_dictionary, id_promotion = working_id_promotion)
		
		"""2""" # retrieving all checked checkbox for current promotion
		campaign_contacts_list = campaign_obj.get_account_list(id_promotion = working_id_promotion)
		logger.debug("selected_contacts_list: " + str(campaign_contacts_list))

                # retrieving paginator object
                try:
                        contacts = paginator.page(page)
                except PageNotAnInteger:
                        # If page is not an integer, deliver first page.
                        contacts = paginator.page(1)
                except EmptyPage:
                        # If page is out of range (e.g. 9999), deliver last page of results.
                        contacts = paginator.page(paginator.num_pages)

                """3""" # creating template context
                context = {
                        'contacts' : contacts,
			'campaign_contacts_list' : campaign_contacts_list,
                        'id_promotion' : working_id_promotion,
			'title': "Seleziona i destinatari",
			'opts': self.model._meta,
			'app_label': self.model._meta.app_label,
                }

                # send promotion (after the senders selection)
                if (request.POST.get("next_step", "")):
                        return HttpResponseRedirect('/admin/website/account/campaigns/step3/' + str(working_id_promotion)) # Redirect after POST

                # select senders list page
                return render(request, 'admin/custom_view/campaigns/step2.html', context)

        # STEP 3
        def campaign_review(self, request, id_promotion=None):

                try:
                        # get add promotion form
                        promotion_obj = Promotion.objects.get(id_promotion=id_promotion)
                        promo_form = PromotionForm(instance=promotion_obj)

                        if (not promotion_obj.status):
                                # checking if user choose to re-edit the promotion
                                if (request.POST.get("edit_promotion", "")):
                                        return HttpResponseRedirect('/admin/website/account/campaigns/step1/') # Redirect after POST

                                # checking if user choose to send the promotion
                                if (request.POST.get("send_promotion", "")):
                                        campaign_obj = Campaign()
                                        campaign_obj.send_campaign(id_promotion)

                                        # redirect to success page
                                        messages.add_message(request, messages.SUCCESS, 'Promozione inviata con successo!')
                                        return HttpResponseRedirect('/admin/website/account/campaigns/step1/1')

                                # count total senders about this campaign
                                campaign_obj = Campaign()
                                total_senders = campaign_obj.count_campaign_senders(id_promotion=id_promotion)

                                # creating template context
                                context = {
                                        'adminform' : promo_form,
                                        'id_promotion' : id_promotion,
                                        'total_senders' : total_senders,
                                        'title': "Riepilogo della campagna",
                                        'opts': self.model._meta,
                                        'app_label': self.model._meta.app_label,
                                }

                                # campaign review page
                                return render(request, 'admin/custom_view/campaigns/step3.html', context)
                        else:
                                # promotion already sent
                                return HttpResponseRedirect('/admin/website/account/campaigns/step1/') # Redirect after POST

                except (KeyError, Promotion.DoesNotExist):
                        # object doesn't exists, id_promotion must exists
                        return HttpResponseRedirect('/admin/website/account/campaigns/step1/1') # Redirect after POST
