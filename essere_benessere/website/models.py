# -*- coding: utf-8 -*-

"""
Simple E/R scheme
=================

        1-N         1-N
Account -> Campaign <- Promotion
"""

from django.db import models
from django.core.mail import send_mail
from django.utils import timezone
import datetime
from datetime import datetime
import string, random, logging

# Get an instance of a logger
logger = logging.getLogger('django.request')

class Account(models.Model):
	id_account = models.AutoField(primary_key=True)
	first_name = models.CharField("Nome", max_length=30)
	last_name = models.CharField("Cognome", max_length=30)
	email = models.EmailField()
	mobile_phone = models.CharField("Numero telefonico", max_length=20)
	birthday_date = models.DateField("Data di nascita", blank=True, null=True)
	receive_promotions = models.BooleanField("Riceve le promozioni", default=0)
	loyal_customer = models.BooleanField("Cliente affezionato", default=0)
	status = models.BooleanField(default=1)

	# On Python 3: def __str__(self):
	def __unicode__(self):
		return str(self.id_account)

class Promotion(models.Model):

        PROMOTION_TYPE_MANUAL = { "key" : "manual", "description" : "Manuale" }
        PROMOTION_TYPE_FRONTEND = { "key" : "frontend_post", "description" : "Pubblica sul frontend" }
        PROMOTION_TYPE_BIRTHDAY = { "key" : "birthday", "description" : "Promozione compleanno" }

	# promotion type selector for admin
	PROMOTION_TYPES_SELECTOR = (
	    (PROMOTION_TYPE_FRONTEND["key"], PROMOTION_TYPE_FRONTEND["description"]),
	    (PROMOTION_TYPE_BIRTHDAY["key"], PROMOTION_TYPE_BIRTHDAY["description"]),
	)

	id_promotion = models.AutoField(primary_key=True)
	name = models.CharField("Titolo promozione", max_length=50)
	description = models.TextField("Contenuto")
        promo_image = models.ImageField("Immagine della promozione", upload_to="/tmp/")
	expiring_date = models.DateField("Scadenza")
	promo_type = models.CharField(max_length=30, choices=PROMOTION_TYPES_SELECTOR)
	status = models.BooleanField(default=0)
	campaigns = models.ManyToManyField(Account, through='Campaign')

	# On Python 3: def __str__(self):
	def __unicode__(self):
		return str(self.id_promotion)

        def get_valid_promotions_list(self, promo_type = PROMOTION_TYPE_FRONTEND["key"]):
                """
                Return a list of valid promotions (not already expired)
                """
                return_var = False

                return return_var

class Campaign(models.Model):
	id_campaign = models.AutoField(primary_key=True)
	id_account = models.ForeignKey(Account, db_column="id_account")
	id_promotion = models.ForeignKey(Promotion, db_column="id_promotion")
	code = models.CharField(max_length=10)
	status = models.BooleanField(default=0)

	# On Python 3: def __str__(self):
	def __unicode__(self):
		return str(self.id_campaign)

        def generate_random_code(self, depth = 0):
                """
                Generating a random promo code, if the generated code already
                exists, than recursively call this function to generate a new ones.
                Max recursion depth: 50
                """

                # generating a random code
                random_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

                try:
                        # checking if code already exists
                        Campaign.objects.get(code=random_code)

                        # than recall this function to generate a new ones
                        if (depth < 50):
                            random_code = Campaign.generate_random_code(self, depth+1)
                        else:
                            logger.error("ATTENZIONE: non sono riuscito a generare un nuovo codice | depth level: " + str(depth))
                            random_code = "PROMOCODE1"

                except (KeyError, Campaign.DoesNotExist):
                        # Yo!
                        pass

                return random_code

        def add_campaign_user(self, id_account=False, id_promotion=False):
                """
                Function to add a row from db, starting from "id_account" and "id_promotion"
                Return true on success
                """

                try:
                        campaign_obj = Campaign.objects.get(id_account=id_account, id_promotion=id_promotion)
                except (KeyError, Campaign.DoesNotExist):
                        campaign_obj = Campaign(
                                            id_account = Account(id_account=id_account),
                                            id_promotion = Promotion(id_promotion=id_promotion),
                                            status = 0
                                        )

                        campaign_obj.save()

                return True

        def remove_campaign_user(self, id_account=False, id_promotion=False):
                """
                Function to delete a row from db, starting from "id_account" and "id_promotion"
                Return true on success
                """

                return_var = False

                try:
                        # retrieve campaign row
                        campaign_obj = Campaign.objects.get(
                                id_account=id_account,
                                id_promotion=id_promotion,
                        )

                        # delete retrieved row from db
                        campaign_obj.delete()

                        return_var = True
                except (KeyError, Campaign.DoesNotExist):
                        # this senders already not exists
                        pass

                return return_var

        def set_campaign_user(self, senders_dictionary = False, id_promotion = False):
                """
                Function to set (or unset) accounts to receive a promotion.
                This function works like this:
                    { "id_account" : 1 } => to enable
                    { "id_account" : 0 } => to disable

                So, for example, if you works with a dictionary like this:
                    { "4" : 1, "5" : 1, "6" : 0, "7" : 1, "8" : 0 }
                You can create previously dictionary with "Campaign.get_senders_dictionary()" function.

                Users 4, 5, 7 will be enabled, while users 6, 8 will be disabled.
                Enabled or disable means row added or removed from db with
                "add_campaign_user" or "remove_campaign_user" functions.
                Return True on success
                """

                if (senders_dictionary and id_promotion):
                        for key, value in senders_dictionary.iteritems():
                                if (value):
                                        self.add_campaign_user(id_account=key, id_promotion=id_promotion)
                                else:
                                        self.remove_campaign_user(id_account=key, id_promotion=id_promotion)

                return True

        def get_checkbox_dictionary(self, paginator_element_list=False, checked_elements=False, checkbox_name=False):
                """
                Function to render a senders dictionary like this:
                { "4" : 1, "5" : 1, "6" : 0, "7" : 1, "8" : 0 }
                Return a checkbox status dictionary on success

                paginator_element_list: all objects in current view (list)
                checked_elements: all checkbox select in current view (list)
                checkbox_name: db column name identifier of every checkbox
                (string) -> es <input type="checkbox" name="checkbox_name[23]" value="1"> 23 is the unique database model ID, like id_account
                """

                checkbox_dictionary = {}

                if (checkbox_name):
                        for element in paginator_element_list:
                                logger.error("models.py: single element " + str(element))
                                # se element è contenuto in checked_elements allora ok
                                if (str(element) in checked_elements):
                                        checkbox_dictionary[str(element)] = 1
                                else:
                                        checkbox_dictionary[str(element)] = 0

                logger.error("models.py, get_senders_dictionary: " + str(checkbox_dictionary))

                return checkbox_dictionary

	def get_account_list(self, id_promotion=False):
		"""
		Function to retrieve all account about a promotion id
		Return an account id list on success
		"""
		
		return_var = []

		if (id_promotion):
			account_list = Campaign.objects.filter(id_promotion=id_promotion)
			for single_element in account_list:
				return_var.append(single_element.id_account.id_account)

			# logger.debug("[get_account_list], account_list: " + str(return_var))

		return return_var

        def count_campaign_senders(self, id_promotion=False):
                """
                Function to count all senders about a campaign
                """

                return_var = 0

                if (id_promotion):
                    return_var = Campaign.objects.filter(id_promotion=id_promotion).count()


                return return_var

        def send_campaign(self, id_promotion=None):
                """
                Function to send a campaing via email
                for all promo sender:
                    -generating a unique random code
                    -sending promo
                """

                return_var = False

                if(id_promotion):
                    senders_list = Campaign.objects.filter(id_promotion=id_promotion)

                    for sender in senders_list:
                            try:
                                    campaign_obj = Campaign.objects.get(id_campaign=sender.id_campaign)

                                    # generating unique random code
                                    random_code = campaign_obj.generate_random_code()
                                    campaign_obj.code = random_code
                                    campaign_obj.save()

                                    # sending campaign via mail
                                    campaign_obj.send_promotional_email(campaign_obj.id_campaign)

                                    return_var = True
                            except(KeyError, Campaign.DoesNotExist):
                                    # id campaign doesn't exists
                                    return_var = False
                                    break

                return return_var

        def get_campaign_details(self, id_campaign=None, campaign_code=None):
                """
                Function to retrieve all details about a campaign.
                Return a dictionary like this:
                    campaign_details = {
                                            'title' : 'promo title',
                                            'content' : 'promo content'
                                            ...
                                        }
                """

                campaign_details = {}
                campaign_obj = None

                try:
                        if (id_campaign):
                                campaign_obj = Campaign.objects.select_related().get(id_campaign=id_campaign)
                        elif (campaign_code):
                                campaign_obj = Campaign.objects.select_related().get(code=campaign_code)

                        if (campaign_obj):
                                promotion_obj = campaign_obj.id_promotion
                                account_obj = campaign_obj.id_account

                                campaign_details["name"] = promotion_obj.name
                                campaign_details["description"] = promotion_obj.description
                                campaign_details["expiring_in"] = promotion_obj.expiring_date
                                campaign_details["image_url"] = promotion_obj.promo_image
                                campaign_details["code"] = campaign_obj.code
                                campaign_details["receiver_email"] = account_obj.email
                                campaign_details["receiver_first_name"] = account_obj.first_name
                                campaign_details["receiver_last_name"] = account_obj.last_name
                except(KeyError, Campaign.DoesNotExist):
                        # id_campaign doesn't exists
                        pass

                return campaign_details

        def send_promotional_email(self, id_campaign=None):
                """
                Function to send a promotion to an email address
                """

                return_var = False

                if (id_campaign is not None):
                        campaign_obj = Campaign()
                        campaign_details = campaign_obj.get_campaign_details(id_campaign=id_campaign)

                        # TODO: buld email body from template
                        html_email = campaign_details["description"] + " | code: " + campaign_details["code"] + " | address: " + campaign_details["receiver_email"]

                        if (campaign_details):
                                send_mail(
                                        campaign_details["name"],
                                        html_email,
                                        'from@example.com',
                                        ['veronesi1231@yahoo.it'],
                                        fail_silently=False
                                )

                logger.error("EMAIL SENT")

                return return_var

        def check_code_validity(self, code, validity_check=None):
                """
                Function to check if a code is not yet used or if the
                promotion isn't expired
                Validity checks available:
                    - not_used
                    - not_expired
                    - exists
                """

                return_var = False

                try:
                        campaign_obj = Campaign.objects.select_related().get(code=code)
                        promotion_obj = campaign_obj.id_promotion

                        if (validity_check == 'not_used'):
                                if ((not campaign_obj.status) or
                                        (promotion_obj.promo_type == Promotion.PROMOTION_TYPE_FRONTEND["key"])):
                                        return_var = True

                        if (validity_check == 'not_expired'):
                                if (promotion_obj.expiring_date >= datetime.now().date()):
                                        return_var = True

                        if (validity_check == 'exists'):
                                if (campaign_obj.id_campaign):
                                        return_var = True

                except(KeyError, Campaign.DoesNotExist):
                        # code not exists
                        pass

                return return_var

        def redeem_code(self, code):
                """
                Function to redeem a coupon code
                """

                return_var = False

                try:
                        # setting code staus = 1 (code used)
                        campaign_obj = Campaign.objects.get(code=code)
                        campaign_obj.status = 1
                        campaign_obj.save()
                        return_var = True

                except(KeyError, Campaign.DoesNotExist):
                        # code not exists
                        pass

                return return_var

