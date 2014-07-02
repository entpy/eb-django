from django.contrib import admin
from website.models import Account,Promotion
from django.conf.urls import patterns
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
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

        # TODO
        def send_campaign(self, request):
                """
                Send campaign wizard view, a custom admin view to enable
                sending promotion to a customer list
                """

                # custom view which should return an HttpResponse
                myForm = super(AccountAdmin, self).get_form(request)
                # logger.debug("admin form: " + str(myForm))
                myList = super(AccountAdmin, self).get_paginator(self, Account.objects.all(), 10)
                page1 = myList.page(1)
                pageLis = page1.object_list
                account_obj = pageLis[0]
                logger.debug("admin list: " + str(account_obj.email))
                template = loader.get_template('admin/custom_view/send_campaign.html')
                context = RequestContext(request, {
                        'account_form': pageLis,
                        'variabile': "ciao",
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
