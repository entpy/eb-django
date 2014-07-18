"""
Common utils class
"""
import calendar
from django.contrib.sites.models import Site

class CommonUtils():

    def get_days_list_choice(self):
            """Get a list of days for select"""
            return range(1, 32)

    def get_months_list_choice(self):
            """Get a list of months for select"""
            months_choices = []
            for i in range(1,13):
                    months_choices.append((i, calendar.month_name[i]))

            return months_choices

    def get_years_list_choice(self):
            """Get a list of years for select"""
            return range(1950, 1998)

    def get_site_url(self):
            # retrieving current site
            Site.objects.clear_cache()
            current_site = Site.objects.get_current()
            return "http://" + current_site.domain
