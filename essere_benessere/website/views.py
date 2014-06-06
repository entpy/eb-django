from django.shortcuts import render

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

def our_works(request):
    return render(request, 'website/our_works.html')

def contacts(request):
    return render(request, 'website/contacts.html')

def pulsed_light(request):
    return render(request, 'website/pulsed_light.html')

def dental_whitening(request):
    return render(request, 'website/dental_whitening.html')

def our_offers(request):
    return render(request, 'website/our_offers.html')

def get_offers(request):
    return render(request, 'website/get_offers.html')
