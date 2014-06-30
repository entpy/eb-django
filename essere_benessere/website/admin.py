from django.contrib import admin
from website.models import Account,Promotion

class AccountAdmin(admin.ModelAdmin):
        fields = (('first_name', 'last_name'), 'email', 'mobile_phone', 'birthday_date', ('receive_promotions', 'loyal_customer'))

class PromotionAdmin(admin.ModelAdmin):
        fields = ('name', 'description', 'promo_image', 'expiring_date', 'promo_type')

        def save_model(self, request, obj, form, change):
                # generate a random code before save data
                obj.code = obj.generate_random_code()
                obj.save()

admin.site.register(Account, AccountAdmin)
admin.site.register(Promotion, PromotionAdmin)
