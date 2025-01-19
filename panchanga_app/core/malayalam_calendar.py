# panchanga_app/core/malayalam_calendar.py

import logging
from datetime import date
from zoneinfo import ZoneInfo  # Also need to import this

logger = logging.getLogger(__name__)

# Malayalam Month Names
MALAYALAM_MONTHS = [
    "Chingam", "Kanni", "Thulam", "Vrischikam", "Dhanu", "Makaram",
    "Kumbham", "Meenam", "Medam", "Edavam", "Mithunam", "Karkidakam"
]

def get_malayalam_month_and_day(sun_longitude):
    """
    Compute the Malayalam month and day based on the Sun's sidereal longitude.
    :param sun_longitude: The Sun's sidereal longitude (0°–360°)
    :return: Tuple (month_name, day_of_month)
    """
    # Each zodiac sign spans 30° sidereal longitude
    zodiac_index = int(sun_longitude // 30)  # 0 = Aries (Medam), ..., 11 = Pisces (Meenam)
    month_name = MALAYALAM_MONTHS[zodiac_index]

    # Day of the month is the degrees within the current zodiac sign
    day_of_month = int(sun_longitude % 30) + 1

    return month_name, day_of_month


def get_kollavarsham_year(gregorian_date, sun_longitude):
    """
    Compute the Kollavarsham year based on the Gregorian date and Sun's sidereal longitude.
    :param gregorian_date: The current Gregorian date
    :param sun_longitude: The Sun's sidereal longitude (0°–360°)
    :return: The Kollavarsham year
    """
    # Chingam 1 (Malayalam New Year) occurs when Sun enters Leo (120°)
    current_year = gregorian_date.year
    chingam_start_longitude = 120  # 120° = Start of Chingam (Leo)

    # Check if the Sun has passed the longitude for Chingam 1 in the current year
    if sun_longitude >= chingam_start_longitude:
        kollavarsham_year = current_year - 825
    else:
        kollavarsham_year = current_year - 826

    return kollavarsham_year

def is_leap_year(year):
    """
    Check if a given year is a leap year in the Gregorian calendar.
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def get_malayalam_date(calculator, sunrise_local, lat, lon):
    """
    Calculate Malayalam date based on sidereal Sun longitude.
    """
    logger.debug(f"Calculating Malayalam date for sunrise: {sunrise_local}, lat={lat}, lon={lon}")

    # Get sidereal Sun longitude
    sidereal_positions = calculator.get_sidereal_positions1(sunrise_local.astimezone(ZoneInfo("UTC")))
    sun_long = sidereal_positions["sun_longitude"]

    # Malayalam months with their standard lengths
    malayalam_months = [
        ("Medam", 30), ("Idavam", 29), ("Mithunam", 30), ("Karkidakam", 29),
        ("Chingam", 30), ("Kanni", 29), ("Thulam", 30), ("Vrischikam", 29),
        ("Dhanu", 29), ("Makaram", 29), ("Kumbham", 29), ("Meenam", 30)
    ]

    # Adjust for leap year (Meenam has 31 days in leap years)
    if is_leap_year(sunrise_local.year):
        malayalam_months[-1] = ("Meenam", 31)  # Update Meenam to 31 days

    # Determine the month and day
    month_index = int(sun_long // 30) % 12
    month_name, month_length = malayalam_months[month_index]

    # Calculate the day within the month
    month_day = int(sun_long % 30) + 1

    # Handle month transitions for overflows (when day > month_length)
    if month_day > month_length:
        next_month_index = (month_index + 1) % 12
        month_name, month_length = malayalam_months[next_month_index]
        month_day = 1
        logger.debug(f"Transitioned to new Malayalam month: {month_name}")

    # Calculate Kollavarsham year
    kollavarsham_year = sunrise_local.year - 825

    logger.debug(f"Malayalam Month: {month_name}, Day: {month_day}, Year: {kollavarsham_year}")
    return {
        "month_name": month_name,
        "month_day": month_day,
        "year": kollavarsham_year
    }
