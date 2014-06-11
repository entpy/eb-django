from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'website.views.index', name='index'),
    url(r'^chi-siamo/', 'website.views.about_us', name='about_us'),
    url(r'^i-nostri-servizi/', 'website.views.our_services', name='our_services'),
    url(r'^contatti/', 'website.views.contacts', name='contacts'),
    url(r'^le-nostre-offerte/', 'website.views.our_offers', name='our_offers'),
    url(r'^ricevi-offerte/', 'website.views.get_offers', name='get_offers'),
    url(r'^luce-pulsata/', 'website.views.pulsed_light', name='pulsed_light'),
    url(r'^sbiancamento-dentale/', 'website.views.dental_whitening', name='dental_whitening'),

    # admin URL
    url(r'^admin/', include(admin.site.urls)),
)
