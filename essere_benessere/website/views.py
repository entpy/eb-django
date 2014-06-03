#from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

def home(request):
    """
        index view
    """
    testo = ""
    for i in range(0,10):
        testo += str(i) + "-"

    template = loader.get_template('website/index.html')
    context = RequestContext(request, {
        'latest_poll_list': 1,
    })
    return HttpResponse(template.render(context))
    #return render(request, 'website/index.html')

def chi_siamo(request):
    return HttpResponse("chi siamo")
    #return render(request, 'website/chi_siamo.html')

def i_nostri_lavori(request):
    return HttpResponse("i nostri lavori")
    #return render(request, 'website/i_nostri_lavori.html')

def contatti(request):
    return HttpResponse("contatti")
    #return render(request, 'website/contatti.html')

def luce_pulsata(request):
    return HttpResponse("luce pulsata")
    #return render(request, 'website/luce_pulsata.html')

def sbiancamento_dentale(request):
    return HttpResponse("sbiancamento dentale")
    #return render(request, 'website/sbiancamento_dentale.html')

def le_nostre_offerte(request):
    return HttpResponse("le nostre offerte")
    #return render(request, 'website/le_nostre_offerte.html')

def ricevi_offerte(request):
    return HttpResponse("ricevi offerte")
    #return render(request, 'website/ricevi_offerte.html')
