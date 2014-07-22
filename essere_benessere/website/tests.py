# -*- coding: utf-8 -*-

import datetime
from django.utils import timezone
from django.test import TestCase
from website.models import Account, Promotion, Campaign

class PollMethodTests(TestCase):

    def test_get_birthday_promotion_instance(self):
        """
        was_published_recently() should return False for polls whose
        pub_date is in the future
        """
        promotion_obj = Promotion()
        promo_instance = promotion_obj.get_birthday_promotion_instance()
        total_birthday_promo = Promotion.objects.filter(promo_type=Promotion.PROMOTION_TYPE_BIRTHDAY["key"]).count()
        if (total_birthday_promo == 0 or total_birthday_promo == 1):
                total_promo_valid = True

        self.assertEqual(total_promo_valid, True)

        # TODO: this test not working
        self.assertEqual(str(promo_instance.promo_type), str(Promotion.PROMOTION_TYPE_BIRTHDAY["key"]))
