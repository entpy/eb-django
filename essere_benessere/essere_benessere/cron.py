# -*- coding: utf-8 -*-

from website.models import Account, Promotion, Campaign
from django_cron import CronJobBase, Schedule
import logging

logger = logging.getLogger('django.request')

class BirthdayPromoCron(CronJobBase):
        RUN_EVERY_MINS = 1 # every 2 hours

        schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
        code = 'essere_benessere.birthday_promo_cron'    # a unique code

        def do(self):
                # Get an instance of a logger
                logger.debug("sending birthday promo...")

                # sending birth
                campaign_obj = Campaign()
                campaign_obj.send_birthday_promotion()
                
                return True
