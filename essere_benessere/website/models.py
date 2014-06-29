"""
Simple E/R scheme
=================

        1-N         1-N
Account -> Campaign <- Promotion
"""

from django.db import models

class Account(models.Model):
	id_account = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.EmailField()
	mobile_phone = models.CharField(max_length=20)
	birthday_date = models.DateField(blank=True, null=True)
	receive_promotions = models.BooleanField(default=0)
	loyal_customer = models.BooleanField(default=0)
	status = models.BooleanField(default=1)

	# On Python 3: def __str__(self):
	def __unicode__(self):
		return self.id_account

class Promotion(models.Model):

	# promotion type selector
	PROMOTION_TYPES = (
	    ('manual', 'Manuale'),
	    ('frontent_post', 'Pubblica sul frontend'),
	    ('birthday', 'Promozione compleanno'),
	)

	id_promotion = models.AutoField(primary_key=True)
	code = models.CharField(max_length=10)
	name = models.CharField(max_length=50)
	description = models.TextField()
	expiring_date = models.DateTimeField()
	promo_type = models.CharField(max_length=30, choices=PROMOTION_TYPES)
	status = models.BooleanField(default=1)
	campaigns = models.ManyToManyField(Account, through='Campaign')

	# On Python 3: def __str__(self):
	def __unicode__(self):
		return self.id_promotion

class Campaign(models.Model):
	id_campaign = models.AutoField(primary_key=True)
	id_account = models.ForeignKey(Account)
	id_promotion = models.ForeignKey(Promotion)
	status = models.BooleanField(default=0)

	# On Python 3: def __str__(self):
	def __unicode__(self):
		return self.id_campaign
