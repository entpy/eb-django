# -*- coding: utf-8 -*-

from django.shortcuts import render
from website.models import Account
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
import datetime
# include constants file
from essere_benessere import constants, functions
from essere_benessere.functions import CommonUtils
import logging

# Get an instance of a logger
logger = logging.getLogger('django.request')

def index(request):
    """
    index view
    """

    """ test only, remove plz
    testo = ""
    for i in range(0,10):
            testo += str(i) + "-"

    template = loader.get_template('website/index.html')
    context = RequestContext(request, {
            'latest_poll_list': 1,
    })
    return HttpResponse(template.render(context))
    """
    return render(request, 'website/index.html')

def about_us(request):
    return render(request, 'website/about_us.html')

def our_services(request):
    return render(request, 'website/our_services.html')

def contacts(request):
    return render(request, 'website/contacts.html')

def pulsed_light(request):
    return render(request, 'website/pulsed_light.html')

def dental_whitening(request):
    return render(request, 'website/dental_whitening.html')

def our_offers(request):
    # TODO: prelevo la lista di offerte presenti in db
    # e le passo context della funzione render
    return render(request, 'website/our_offers.html')

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
				logger.debug('Nuovo utente, inserisco in db')
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
					# logger.error("Errore con il salvataggio della data o data non inserita")
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
			messages.add_message(request, messages.ERROR, 'Per continuare è necessario inserire una mail e confermare la privacy.')
			logger.debug('Attenzione: inserire email e/o confermare disclaimer')
	else:
		logger.debug('Attenzione: submit del form non ancora eseguito')


	"""
	try:
	account = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
	# Redisplay the poll voting form.
	return render(request, 'polls/detail.html', {
	    'poll': p,
	    'error_message': "You didn't select a choice.",
	})
	else:
	selected_choice.votes += 1
	selected_choice.save()
	# Always return an HttpResponseRedirect after successfully dealing
	# with POST data. This prevents data from being posted twice if a
	# user hits the Back button.
	return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
	"""

	return render(request, 'website/get_offers.html', context)
