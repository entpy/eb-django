from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'website.views.home', name='home'),
    url(r'^chi-siamo/', 'website.views.chi_siamo', name='chi_siamo'),
    url(r'^i-nostri-lavori/', 'website.views.i_nostri_lavori', name='i_nostri_lavori'),
    url(r'^contatti/', 'website.views.contatti', name='contatti'),
    url(r'^le-nostre-offerte/', 'website.views.le_nostre_offerte', name='le_nostre_offerte'),
    url(r'^ricevi-offerte/', 'website.views.ricevi_offerte', name='ricevi_offerte'),
    url(r'^luce-pulsata/', 'website.views.luce_pulsata', name='luce_pulsata'),
    url(r'^sbiancamento-dentale/', 'website.views.sbiancamento_dentale', name='sbiancamento_dentale'),

    # admin URL
    url(r'^admin/', include(admin.site.urls)),
)
