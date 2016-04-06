# -*- coding: utf-8 -*-

from website.models import Account, Promotion, Campaign
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.core.urlresolvers import reverse
from django.contrib import messages
import datetime
# include constants file
from essere_benessere import constants, functions
from essere_benessere.functions import CommonUtils
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
        return render(request, 'website/index.html')

def about_us(request):
        return render(request, 'website/about_us.html')

def our_services(request):
        return render(request, 'website/our_services.html')

def contacts(request):
        return render(request, 'website/contacts.html')

def dental_whitening(request):
        return render(request, 'website/dental_whitening.html')

def terms_of_use(request):
        return render(request, 'website/terms_of_use.html')

def our_offers(request):

        promotion_obj = Promotion()

        # list of all valid promotion (not expired) with type = frontend_post
        valid_promotion_dict = promotion_obj.get_valid_promotions_list()

        context = {
                'promotion_list' : valid_promotion_dict,
        }

        return render(request, 'website/our_offers.html', context)

@ensure_csrf_cookie
def get_offers(request):

	CommonUtilsInstance = CommonUtils()
	# built of date selector
	# days list
	days_choices = CommonUtilsInstance.get_days_list_choice()
	# months list
	months_choices = CommonUtilsInstance.get_months_list_choice()
	# years list
	years_choices = CommonUtilsInstance.get_years_list_choice()

	context = {
		"post" : request.POST,
		"days_choices" : days_choices,
		"months_choices" : months_choices,
		"years_choices" : years_choices,
	}

	# se la mail dell'utente non esiste inserisco i dati
	# altrimenti per il momento non permetto la modifica di una mail gia esistente
	if (request.POST.get("get_offers_form_sent", "")):
		if(request.POST.get("email", "") and request.POST.get("disclaimer", "")):
			try:
				account_obj = Account.objects.get(email=request.POST['email'])
			except (KeyError, Account.DoesNotExist):
				logger.debug('nuovo utente registrato: ' + str(request.POST['email']))
				account_obj = Account(
					first_name = request.POST['first_name'],
					last_name = request.POST['last_name'],
					email = request.POST['email'],
					mobile_phone = request.POST['phone'],
					receive_promotions = 1,
				)

				try:
					birthday = datetime.date(int(request.POST['birthday_year']),
                                                    int(request.POST['birthday_month']),
                                                    int(request.POST['birthday_day'])
					)
					account_obj.birthday_date = birthday
				except:
					logger.debug("Errore con il salvataggio della data o data non inserita")
					pass

				# saving account information
				account_obj.save()

				# if user successfully inserted, than showing a success message
				messages.add_message(request, messages.SUCCESS, 'Grazie per esserti registrato!')
				return HttpResponseRedirect(reverse(get_offers))
			else:
				messages.add_message(request, messages.ERROR, "Attenzione utente già esistente")
				logger.debug("Utente gia' esistente in db")
		else:
			messages.add_message(request, messages.ERROR, 'Per continuare è necessario inserire una mail e confermare il trattamento dei dati personali.')
			logger.debug('Attenzione: inserire email e/o confermare disclaimer')
	else:
		logger.debug('Attenzione: submit del form non ancora eseguito')
		pass

	return render(request, 'website/get_offers.html', context)
