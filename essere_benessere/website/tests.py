# -*- coding: utf-8 -*-

from django.utils import timezone
from django.test import TestCase
from website.models import Account, Promotion, Campaign
import datetime, logging

# Get an instance of a logger
logger = logging.getLogger('django.request')

class PromotionMethodTests(TestCase):

    def test_get_birthday_promotion_instance(self):
        """
        get_birthday_promotion_instance() should return:
        - only one promo (if exists)
        - with promo_type="birthday"
        """

        promotion_obj = Promotion()
        promo_instance = promotion_obj.get_birthday_promotion_instance()
        logger.error("retrieved promo type: " + str(Promotion.PROMOTION_TYPE_BIRTHDAY["key"]))
        total_birthday_promo = Promotion.objects.filter(promo_type=Promotion.PROMOTION_TYPE_BIRTHDAY["key"]).count()
        if (total_birthday_promo == 0 or total_birthday_promo == 1):
                total_promo_valid = True

        self.assertEqual(total_promo_valid, True)

        # TODO: this test not working (why whyyyy?)
        self.assertEqual(str(promo_instance.promo_type), str(Promotion.PROMOTION_TYPE_BIRTHDAY["key"]))
