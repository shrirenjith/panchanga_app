# panchanga_app/core/ayanamsa.py

from datetime import date

class AyanamsaCalculator:
    """
    Class to calculate Ayanamsa (sidereal correction) for a given date.

    Supports both regular year-based precision and fractional-year precision.
    """

    def __init__(self, epoch_year=285, precession_rate=50.3):
        """
        Initialize the AyanamsaCalculator with default values.
        :param epoch_year: The year when tropical and sidereal zodiacs aligned (default: 285 CE).
        :param precession_rate: Precession rate in arcseconds per year (default: 50.3).
        """
        self.epoch_year = epoch_year
        self.precession_rate = precession_rate

    def calculate(self, date_obj, use_fractional=False):
        """
        Calculate the Ayanamsa for the given date.
        :param date_obj: A datetime.date object (Gregorian date).
        :param use_fractional: Whether to use fractional-year precision (default: False).
        :return: Ayanamsa in degrees.
        """
        if use_fractional:
            return self._calculate_fractional(date_obj)
        else:
            return self._calculate_regular(date_obj)

    def _calculate_regular(self, date_obj):
        """
        Calculate Ayanamsa using regular year-based precision.
        :param date_obj: A datetime.date object.
        :return: Ayanamsa in degrees.
        """
        # Number of years since the epoch
        years_since_epoch = date_obj.year - self.epoch_year

        # Precession in arcseconds
        total_precession_arcseconds = years_since_epoch * self.precession_rate

        # Convert arcseconds to degrees
        return total_precession_arcseconds / 3600

    def _calculate_fractional(self, date_obj):
        """
        Calculate Ayanamsa using fractional-year precision.
        :param date_obj: A datetime.date object.
        :return: Ayanamsa in degrees.
        """
        # Days in the year for the given date (account for leap years)
        days_in_year = 366 if (date_obj.year % 4 == 0 and (date_obj.year % 100 != 0 or date_obj.year % 400 == 0)) else 365

        # Fraction of the year passed
        day_of_year = date_obj.timetuple().tm_yday
        fractional_year = date_obj.year + (day_of_year / days_in_year)

        # Years since the epoch
        years_since_epoch = fractional_year - self.epoch_year

        # Precession in arcseconds
        total_precession_arcseconds = years_since_epoch * self.precession_rate

        # Convert arcseconds to degrees
        return total_precession_arcseconds / 3600
