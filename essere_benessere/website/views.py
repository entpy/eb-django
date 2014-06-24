from django.shortcuts import render
from website.models import Account
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
	return render(request, 'website/our_offers.html')

def get_offers(request):
	# se la mail dell'utente non esiste inserisco i dati
	# altrimenti per il momento non permetto la modifica di una mail gia esistente

	if (request.POST.get("get_offers_form_sent", "")):
		if(request.POST.get("email", "") and request.POST.get("disclaimer", "")):
			try:
				account_obj = Account.objects.get(email=request.POST['email'])
			except (KeyError, Account.DoesNotExist):
				logger.debug('Nuovo utente, inserisco in db')
			else:
				logger.debug("Utente gia' esistente in db")
		else:
			logger.debug('Attenzione: inserire email e confermare disclaimer')
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

	return render(request, 'website/get_offers.html')
