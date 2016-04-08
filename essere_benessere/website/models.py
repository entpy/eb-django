# -*- coding: utf-8 -*-

"""
Simple E/R scheme
=================

        1-N         1-N
Account -> Campaign <- Promotion

aggiungo 'sent' in Campaign, default a 0
genero il codice in 'add_campaign_user' e non in 'send_campaign'
per questo tipo di promozione, forzo l'inserimento in campagne
in 'send_campaign' filtro solo gli utenti di quella campagna con sent = 0
(ancora da inviare) e setto 'sent=1'
"""

from django.db import models
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from django.utils.html import format_html, mark_safe
from essere_benessere.functions import CommonUtils
from essere_benessere.CustomImagePIL import CustomImagePIL
import datetime, string, random, logging, sys
from datetime import datetime

# TODO: delete also model image with post_delete signal
# more info here: https://docs.djangoproject.com/en/1.6/topics/signals/

# force utf8 read data
reload(sys);
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Account(models.Model):
	id_account = models.AutoField(primary_key=True)
	first_name = models.CharField("Nome", max_length=30)
	last_name = models.CharField("Cognome", max_length=30)
	email = models.EmailField()
	mobile_phone = models.CharField("Numero telefonico", max_length=20, blank=True, null=True)
	birthday_date = models.DateField("Data di nascita", blank=True, null=True)
	receive_promotions = models.BooleanField("Riceve le promozioni", default=0)
	loyal_customer = models.BooleanField("Cliente affezionato", default=0)
	status = models.BooleanField(default=1)

	class Meta:
		verbose_name = "Utente"
		verbose_name_plural = "Utenti"

	# On Python 3: def __str__(self):
	def __unicode__(self):
		return str(self.email)

        def get_birthday_account(self):
                """ List of all users who make birthday today """
                return_var = None
                return_var = Account.objects.filter(
                    birthday_date__month=datetime.now().date().month,
                    birthday_date__day=datetime.now().date().day
                )

                return return_var

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
        promo_image = models.ImageField("Immagine della promozione", upload_to="promo_images/")
	expiring_date = models.DateField("Scadenza", null=True)
	promo_type = models.CharField(max_length=30, choices=PROMOTION_TYPES_SELECTOR)
	status = models.BooleanField(default=0)
	campaigns = models.ManyToManyField(Account, through='Campaign')

	# custom model options
	class Meta:
		verbose_name = "Promozione"
		verbose_name_plural = "Promozioni"

	# On Python 3: def __str__(self):
	def __unicode__(self):
		return str(self.name)

        def save(self, *args, **kwargs):
                """
                Overriding save method to handle uploaded image
                """

                # saving model
                super(Promotion, self).save(*args, **kwargs) # Call the "real" save() method.

                # resize image
                img_file_name = str(self.promo_image.path)
                custom_image_PIL_obj = CustomImagePIL(file_path=img_file_name)
                custom_image_PIL_obj.resize_image(filename=self.promo_image.path)

        def get_valid_promotions_list(self, promo_type = PROMOTION_TYPE_FRONTEND["key"]):
                """
                Return a list of valid promotions (not expired yet)
                """

                valid_promotion_list = []
                campaign_obj = Campaign()

                # list of all promotion valid (queryset starts from campaign object)
                filtered_promotions = Campaign.objects.filter(
                        id_promotion__promo_type=promo_type).filter(
                        id_promotion__expiring_date__gte=datetime.now().date()
                )

                # for every campaign retrieving promo details
                if (filtered_promotions):
                        for valid_promo in filtered_promotions:
                                # retrieving valid campaign id
                                id_valid_campaign = valid_promo.id_campaign
                                # build dictionary with promotion details
                                valid_promotion_list.append(campaign_obj.get_campaign_details(id_campaign=id_valid_campaign))

                return valid_promotion_list

        def delete_birthday_promotion(self):
                """
                Function to delete a birthday promotion
                """

                return_var = False

                try:
                        # retrieve birthday promotion
                        # NB: exists only one promotion with type = birthday
                        promotion_obj = Promotion.objects.get(promo_type=self.PROMOTION_TYPE_BIRTHDAY["key"])

                        # delete retrieved row from db
                        promotion_obj.delete()

                        return_var = True
                except (KeyError, Promotion.DoesNotExist):
                        # birthday promo not exists yet
                        pass

                return return_var

        def get_birthday_promotion_instance(self):
                """
                Function to retrieve a birtyday promotion obj
                Return id_promotion birthday on success, None otherwise
                """

                return_var = None

                try:
                        # retrieve birthday promotion
                        # NB: exists only one promotion with type = birthday
                        promotion_obj = Promotion.objects.get(promo_type=self.PROMOTION_TYPE_BIRTHDAY["key"])
                        return_var = promotion_obj
                except (KeyError, Promotion.DoesNotExist):
                        # birthday promo not exists yet
                        pass

                return return_var

class Campaign(models.Model):
	id_campaign = models.AutoField(primary_key=True)
	id_account = models.ForeignKey(Account, db_column="id_account", null=True)
	id_promotion = models.ForeignKey(Promotion, db_column="id_promotion")
	code = models.CharField(max_length=10)
	status = models.BooleanField(default=0)
	sent = models.BooleanField(default=0)

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
                random_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

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

        def add_frontend_post_campaign(self, id_promotion=None):
                """
                Function to add a campaign for frontend_post campaign
                """
                campaign_obj = Campaign()
                return_var = False

                if id_promotion:
                    if not Campaign.objects.filter(id_promotion__id_promotion=id_promotion).exists():
                        # if a campaign code does not exists yet, then creating a new ones
                        campaign_obj = Campaign(
                            id_promotion = Promotion(id_promotion=id_promotion),
                            code = campaign_obj.generate_random_code(),
                            sent = 1
                        )
                        campaign_obj.save()
                        return_var = True

                return return_var

        def add_campaign_user(self, id_account=False, id_promotion=False, force_insert=False):
                """
                Function to add a row from db, starting from "id_account" and "id_promotion"
                Return true on success
                """
                create_campaign = False

                if not Campaign.objects.filter(id_account=id_account, id_promotion=id_promotion).exists():
                    # creo la campagna e genero un codice random
                    create_campaign = True

                if create_campaign or force_insert:
                    # l'inserimento forzato è per le promozioni compleanno
                    campaign_obj = Campaign(
                        id_account = Account(id_account=id_account),
                        id_promotion = Promotion(id_promotion=id_promotion),
                        code = self.generate_random_code()
                    )
                    campaign_obj.save()

                return True

        # TODO: testare rimozione/inserimento utenti nel flow della promozione
        def remove_campaign_user(self, id_account=False, id_promotion=False):
                """
                Function to delete rows from db, starting from "id_account" and "id_promotion"
                Return true on success
                """
                # delete all row about this account and promotion
                campaign_obj = Campaign.objects.filter(
                    id_account=id_account,
                    id_promotion=id_promotion,
                ).delete()

                return True

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
                                # se element è contenuto in checked_elements allora ok
                                if (str(element.id_account) in checked_elements):
                                        checkbox_dictionary[str(element.id_account)] = 1
                                else:
                                        checkbox_dictionary[str(element.id_account)] = 0

                # logger.error("models.py, get_senders_dictionary: " + str(checkbox_dictionary))

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

        def send_campaign(self, id_promotion):
                """
                Function to send a campaing via email
                for all promo sender:
                    -generating a unique random code
                    -sending promo
                """

                return_var = False

                if id_promotion:
                    # filtro gli utenti di questa campagna che possono ricevere la mail (sent=0)
                    senders_list = Campaign.objects.filter(id_promotion=id_promotion, sent=0)

                    for sender in senders_list:
                            try:
                                campaign_obj = Campaign.objects.get(id_campaign=sender.id_campaign)
                            except(KeyError, Campaign.DoesNotExist):
                                # id campaign doesn't exist
                                return_var = False
                                break
                            else:
                                # setto la campagna come non utilizzata
                                campaign_obj.status = 0
                                # setto la campagna come inviata
                                campaign_obj.sent = 1
                                campaign_obj.save()
                                # sending campaign via mail
                                campaign_obj.send_promotional_email(id_campaign=campaign_obj.id_campaign)
                                return_var = True

                return return_var

        def get_campaign_details(self, id_campaign=None, campaign_code=None):
                """
                Function to retrieve all details about a campaign.
		First by id_campaign, if id_campaign is null campaign_code will
		be used.
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

                                # retrieving custom expiring in string (frontend or backend)
                                expiring_in_days = campaign_obj.get_expiring_in_days(campaign_details["expiring_in"])
                                campaign_details["expiring_in_readable_frontend"] = campaign_obj.get_expiring_in_text(expiring_in_days)
                                campaign_details["expiring_in_readable_backend"] = campaign_obj.get_expiring_in_text(expiring_in_days, True)

                                campaign_details["image_relative_path"] = promotion_obj.promo_image.url
                                campaign_details["code"] = campaign_obj.code
                                # a frontend_post promotion has not recipients
                                if (account_obj):
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

                        if (campaign_details):

                                # building email html
                                html_body = campaign_obj.build_email_html(campaign_details_dict=campaign_details)

                                msg = EmailMessage(campaign_details["name"], html_body, 'info@esserebenesserebeauty.it', [campaign_details["receiver_email"]])
                                msg.content_subtype = "html"  # Main content is now text/html
                                msg.send()

                logger.error("EMAIL SENT TO: " + campaign_details["receiver_email"])

                return return_var

        def build_email_html(self, campaign_details_dict=None):
                """
                Function to build email html from campaign details dictionary
                """

                return_var = ""
                campaign_obj = Campaign()
                common_utils_obj = CommonUtils()

                if (campaign_details_dict):

                        # loading HTML template from file
                        f = open(settings.ABSOLUTE_WEBSITE_STATIC_DIR + 'email_template.html', 'r')
                        html_template = f.read()

                        # bulding email body from template previously loaded
                        """
                            {0} = title
                            {1} = description
                            {2} = code
                            {3} = expiring_in_readable_backend
                            {4} = image_url
                            {5} = site_static_url
                            {6} = facebook_page_url
                            {7} = site_url
                        """

                        logger.error("image URL: " + str(common_utils_obj.get_site_url() + str(campaign_details_dict["image_relative_path"])))
                        # sobstitute var inside html template
                        return_var = format_html (
                                html_template,
                                campaign_details_dict["name"], # promo title
                                mark_safe(campaign_details_dict["description"]), # promo description
                                campaign_details_dict["code"], # promo code
                                mark_safe(campaign_details_dict["expiring_in_readable_backend"]), # promo expiring in days
                                common_utils_obj.get_site_url() + str(campaign_details_dict["image_relative_path"]), # promot image URL
                                common_utils_obj.get_site_url() + settings.STATIC_URL + "website/img/", # site static URL
                                "", # facebook page url
                                common_utils_obj.get_site_url(), # site URL
                        )

                return return_var

        def get_expiring_in_text(self, expiring_in_days=None, is_frontend=False):
                """
                Function to build a string about promotion expiring in
                """

                expiring_in_string = ""

                if (is_frontend):
                        if (expiring_in_days == 0):
                            expiring_in_string = "<br /><b>Approfittane subito, l'offerta scade OGGI!</b>"
                        if (expiring_in_days == 1):
                            expiring_in_string = "<br /><b>Approfittane subito, l'offerta scade domani!</b>"
                        elif (expiring_in_days > 1):
                            expiring_in_string = "<br /><b>Approfittane subito, l'offerta scade tra " + str(expiring_in_days) + " giorni</b>"
                else:
                        if (expiring_in_days == 0):
                            expiring_in_string = "L'offerta scade <span class=\"expiring_today\">OGGI</span>!"
                        if (expiring_in_days == 1):
                            expiring_in_string = "L'offerta scade domani!"
                        elif (expiring_in_days > 1):
                            expiring_in_string = "L'offerta scade tra " + str(expiring_in_days) + " giorni"

                return expiring_in_string

        def check_code_validity(self, code, validity_check=None):
                """
                Function to check if a code is not used yet or if the
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
                                if ((not campaign_obj.status) or (promotion_obj.promo_type == Promotion.PROMOTION_TYPE_FRONTEND["key"])):
                                        return_var = True

                        if (validity_check == 'not_expired'):
                                if ((promotion_obj.expiring_date is None) or (promotion_obj.expiring_date >= datetime.now().date())):
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
                        # setting code status = 1 (code used)
                        campaign_obj = Campaign.objects.get(code=code)
                        campaign_obj.status = 1
                        campaign_obj.save()
                        return_var = True
			logger.info("codice " + str(code) + " validato con successo")

                except(KeyError, Campaign.DoesNotExist):
                        # code not exists
                        pass

                return return_var

        def get_expiring_in_days(self, expiring_date=None):
                """
                Function to calculate expiring in between two date
                """

                return_var = None

                if (expiring_date):
                        return_var = (expiring_date - datetime.now().date()).days

                return return_var

        def send_birthday_promotion(self):
                """
                Function to send a promotional email to users who have a birthday today
                """

                account_obj = Account()
                promotion_obj = Promotion()
                campaign_obj = Campaign()

                # list of all users whoget_birthday_account make birthday today
                account_list = account_obj.get_birthday_account()

                # retrieving birthday promotion
                birthday_promo = promotion_obj.get_birthday_promotion_instance()

                # for everyone sending a promotional email
                if (account_list and birthday_promo):
			logger.info("birthday promo can be sent (birthday promo id #" + str(birthday_promo.id_promotion) + ")")
                        for single_account in account_list:
                                logger.info("send birthday promo to account id #" + str(single_account.id_account))
                                campaign_obj.add_campaign_user(id_account=single_account.id_account, id_promotion=birthday_promo.id_promotion, force_insert=True)
                                campaign_obj.send_campaign(id_promotion=birthday_promo.id_promotion)

                return True
