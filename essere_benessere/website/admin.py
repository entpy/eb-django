from django.contrib import admin
from website.models import Account,Promotion
from django.conf.urls import patterns
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging

# Get an instance of a logger
logger = logging.getLogger('django.request')

class AccountAdmin(admin.ModelAdmin):
        # fileds in add/modify form
        fields = (('first_name', 'last_name'), 'email', 'mobile_phone', 'birthday_date', ('receive_promotions', 'loyal_customer'))

        # URLs overwriting to add new admin views (with auth check and without cache)
        def get_urls(self):
            urls = super(AccountAdmin, self).get_urls()
            my_urls = patterns('',
                    (r'^send_campaign/$', self.admin_site.admin_view(self.send_campaign))
            )

            # return custom URLs with default URLs
            return my_urls + urls

        def send_campaign(self, request):
                """
                Send campaign wizard view, a custom admin view to enable
                sending promotion to a customer list
                """

                contact_list = Account.objects.all()
                paginator = Paginator(contact_list, 5)

                # TODO list 
                """
                1:{
                    saving checked and delete unchecked checkbox from form into
                    db/session if POST exists (fare una funzione che prenda una serie di id
                    e li salvi/elimini, se l'id è presente lo aggiungo, se
                    l'id non è presente lo elimino, sulla base del query_set
                    "contact_list" )
                }

                2:{
                    retrieving checked checkbox from db/session
                }
                
                3:{
                    passing checked checkbox to template context
                }

                4:{
                    # get paginator page number, if exists
                    if request.POST.get('previous') exists
                        then page = request.POST.get('previous_page_number') contain previously page number
                    else if request.POST.get('next') exists
                        then page = request.POST.get('next_page_number') contain next page number
                }
                """

                # default page number
                page = 2

                # 1 TODO: set/unset campaign senders
                senders_dictionary = Campaign.get_senders_dictionary(paginator.page(page), request.POST.get('contacts'))

                logger.debug("selected customers post: " + str(request.POST))

                # retrieving paginator object
                try:
                        contacts = paginator.page(page)
                except PageNotAnInteger:
                        # If page is not an integer, deliver first page.
                        contacts = paginator.page(1)
                except EmptyPage:
                        # If page is out of range (e.g. 9999), deliver last page of results.
                        contacts = paginator.page(paginator.num_pages)

                # custom view which should return an HttpResponse
                # myForm = super(AccountAdmin, self).get_form(request)
                # logger.debug("admin form: " + str(myForm))
                # myList = super(AccountAdmin, self).get_paginator(self, Account.objects.all(), 10)
                # page1 = myList.page(1)
                # pageLis = page1.object_list
                # account_obj = pageLis[0]
                # logger.debug("admin list: " + str(account_obj.email))

                # loading template
                template = loader.get_template('admin/custom_view/send_campaign.html')

                # creating template context
                context = RequestContext(request, {
                        'contacts': contacts,
                })

                return HttpResponse(template.render(context))

class PromotionAdmin(admin.ModelAdmin):
        # fileds in add/modify form
        fields = ('name', 'description', 'promo_image', 'expiring_date', 'promo_type')

        def save_model(self, request, obj, form, change):
                # generating a random code before save data
                obj.code = obj.generate_random_code()
                obj.save()

# registering models to admin interface
admin.site.register(Account, AccountAdmin)
admin.site.register(Promotion, PromotionAdmin)
