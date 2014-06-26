"""
Common utils class
"""

class CommonUtils():

    def get_days_list_choice():
        """Get a list of days for select"""
        return range(1, 32)

    def get_months_list_choice():
        """Get a list of months for select"""
        months_choices = []
        for i in range(1,13):
            # TODO: capire quali librerie includere per questo
            months_choices.append((i, calendar.month_name[i]))

            return months_choices

    def get_years_list_choice():
        """Get a list of years for select"""
        return range(1950, 1998)
