# -*- coding: utf-8 -*-

"""
Simple E/R scheme
=================

        1-N         1-N
Account -> Campaign <- Promotion
"""

from django.db import models
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
	code = models.CharField(max_length=10)
	name = models.CharField("Titolo promozione", max_length=50)
	description = models.TextField("Contenuto")
        promo_image = models.ImageField("Immagine della promozione", upload_to="/tmp/")
	expiring_date = models.DateField("Scadenza")
	promo_type = models.CharField(max_length=30, choices=PROMOTION_TYPES_SELECTOR)
	status = models.BooleanField(default=1)
	campaigns = models.ManyToManyField(Account, through='Campaign')

	# On Python 3: def __str__(self):
	def __unicode__(self):
		return str(self.id_promotion)

        def generate_random_code(self, depth = 0):
                """
                Generating a random promo code, if the generated code already
                exists, than recursively call this function to generate a ne ones.
                Max recursion depth: 50
                """

                # generating a random code
                random_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

                try:
                        # checking if code already exists
                        Promotion.objects.get(code=random_code)

                        # than recall this function to generate a new ones
                        if (depth < 50):
                            random_code = Promotion.generate_random_code(self, depth+1)
                        else:
                            logger.error("ATTENZIONE: non sono riuscito a generare un nuovo codice | depth level: " + str(depth))
                            random_code = "PROMOCODE1"

                except (KeyError, Promotion.DoesNotExist):
                        # Yo!
                        pass

                return random_code

        def get_valid_promotions_list(self, promo_type = PROMOTION_TYPE_FRONTEND["key"]):
                """
                Return a list of valid promotions (not already expired)
                """
                return_var = False

                return return_var

class Campaign(models.Model):
	id_campaign = models.AutoField(primary_key=True)
	id_account = models.ForeignKey(Account)
	id_promotion = models.ForeignKey(Promotion)
	status = models.BooleanField(default=0)

	# On Python 3: def __str__(self):
	def __unicode__(self):
		return str(self.id_campaign)
