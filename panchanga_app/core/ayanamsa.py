from datetime import date
from functools import lru_cache

class AyanamsaCalculator:
    """
    Class to calculate Ayanamsa (sidereal correction) for a given date.

    Supports both regular year-based precision and fractional-year precision.
    """

    SECONDS_IN_A_DEGREE = 3600
    DAYS_IN_COMMON_YEAR = 365
    DAYS_IN_LEAP_YEAR = 366

    def __init__(self, epoch_year=285, precession_rate=50.3):
        """
        Initialize the AyanamsaCalculator with default values.
        :param epoch_year: The year when tropical and sidereal zodiacs aligned (default: 285 CE).
        :param precession_rate: Precession rate in arcseconds per year (default: 50.3).
        """
        self.epoch_year = epoch_year
        self.precession_rate = precession_rate

    @lru_cache(maxsize=128)
    def calculate(self, date_obj, use_fractional=False):
        """
        Calculate the Ayanamsa for the given date.
        :param date_obj: A datetime.date object (Gregorian date).
        :param use_fractional: Whether to use fractional-year precision (default: False).
        :return: Ayanamsa in degrees.
        """
        if date_obj.year < 1582:
            raise ValueError("The input date must be in the Gregorian calendar (after 1582 CE).")

        if use_fractional:
            return self._calculate_fractional(date_obj)
        else:
            return self._calculate_regular(date_obj)

    def _calculate_regular(self, date_obj):
        """
        Calculate Ayanamsa using regular year-based precision.
        """
        years_since_epoch = date_obj.year - self.epoch_year
        total_precession_arcseconds = years_since_epoch * self.precession_rate
        return total_precession_arcseconds / self.SECONDS_IN_A_DEGREE

    def _calculate_fractional(self, date_obj):
        """
        Calculate Ayanamsa using fractional-year precision.
        """
        days_in_year = self.DAYS_IN_LEAP_YEAR if (date_obj.year % 4 == 0 and (date_obj.year % 100 != 0 or date_obj.year % 400 == 0)) else self.DAYS_IN_COMMON_YEAR
        fractional_year = date_obj.year + (date_obj.timetuple().tm_yday / days_in_year)
        years_since_epoch = fractional_year - self.epoch_year
        total_precession_arcseconds = years_since_epoch * self.precession_rate
        return total_precession_arcseconds / self.SECONDS_IN_A_DEGREE
