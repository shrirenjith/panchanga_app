 # panchanga_app/core/lookup_service.py

import logging
from datetime import timedelta
from fractions import Fraction

logger = logging.getLogger(__name__)

# Tithi Names
TITHI_NAMES = {
    "english": [
        "Prathama", "Dvitiya", "Trtiya", "Chaturthi", "Panchami", "Shashti",
        "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dvadashi",
        "Trayodashi", "Chaturdashi", "Pournami",  # Shukla Paksha
        "Prathama", "Dvitiya", "Trtiya", "Chaturthi", "Panchami", "Shashti",
        "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dvadashi",
        "Trayodashi", "Chaturdashi", "Amavasya"  # Krishna Paksha
    ],
    "malayalam": [
        "പ്രഥമ", "ദ്വിതീയ", "തൃതീയ", "ചതുര്‍ത്ഥി", "പഞ്ചമി", "ഷഷ്ഠി",
        "സപ്തമി", "അഷ്ടമി", "നവമി", "ദശമി", "എകാദശി", "ദ്വാദശി",
        "ത്രയോദശി", "ചതുര്ദശി", "പൗര്‍ണമി",  # Shukla Paksha
        "പ്രഥമ", "ദ്വിതീയ", "തൃതീയ", "ചതുര്‍ത്ഥി", "പഞ്ചമി", "ഷഷ്ഠി",
        "സപ്തമി", "അഷ്ടമി", "നവമി", "ദശമി", "എകാദശി", "ദ്വാദശി",
        "ത്രയോദശി", "ചതുര്ദശി", "അമാവാസ്യ"  # Krishna Paksha
    ]
}

# Nakshatra Names
NAKSHATRA_NAMES = {
    "english": [
        "Ashwati", "Bharani", "Karthika", "Rohini", "Makayiram", "Thiruvathira",
        "Punartham", "Pooyam", "Ayilyam", "Makam", "Pooram", "Uthram",
        "Atham", "Chithira", "Chothi", "Visakham", "Anizham", "Thrikketta",
        "Moolam", "Pooradam", "Uthradam", "Thiruvonam", "Avittam", "Chatayam",
        "Pururuttathi", "Uthrittathi", "Revathi"
    ],
    "malayalam": [
        "അശ്വതി", "ഭരണി", "കാര്‍ത്തിക", "രോഹിണി", "മകയിരം", "തിരുവാതിര",
        "പുനര്‍തം", "പൂയം", "അയില്യം", "മകം", "പൂരം", "ഉത്രം",
        "അത്തം", "ചിത്ര", "ചോതി", "വിശാഖം", "അനിഴം", "തൃക്കേട്ട",
        "മൂലം", "പൂരാടം", "ഉത്രാടം", "തിരുവോണം", "അവിട്ടം", "ചതയം",
        "പൂര്‍രുട്ടാതി", "ഉത്രട്ടാതി", "രേവതി"
    ]
}

def get_tithi_name(tithi_idx, language="english"):
    """
    Fetch Tithi name in the specified language.
    :param tithi_idx: Index of the Tithi (0-29)
    :param language: "english" or "malayalam"
    :return: Tithi name as a string
    """
    return TITHI_NAMES[language][tithi_idx]

def get_nakshatra_name(nakshatra_idx, language="english"):
    """
    Fetch Nakshatra name in the specified language.
    :param nakshatra_idx: Index of the Nakshatra (0-26)
    :param language: "english" or "malayalam"
    :return: Nakshatra name as a string
    """
    return NAKSHATRA_NAMES[language][nakshatra_idx]


# Function to dynamically calculate Nakshatra timings
def calculate_nakshatra_timings(moon_lon, sunrise_local, eph_calc):
    """
    Calculate Nakshatra timings for the given day and beyond, based on the Moon's longitude.
    :param moon_lon: Initial Moon sidereal longitude at local sunrise.
    :param sunrise_local: Sunrise time in local time.
    :param eph_calc: Instance of EphemerisCalculator for Moon's motion.
    :return: List of dictionaries with Nakshatra timings and names in local time.
    """
    logger.debug(f"Calculating Nakshatra timings starting with Moon longitude: {moon_lon}")

    nakshatra_degrees = 360.0 / 27.0  # Each Nakshatra spans 13°20'
    moon_daily_motion = 13.1667      # Average Moon motion per day (in degrees)
    results = []

    current_time = sunrise_local
    current_nakshatra_index = int(moon_lon // nakshatra_degrees)

    while len(results) < 5:  # Arbitrarily calculate the next 5 transitions
        # Get current Nakshatra names
        current_nakshatra_name_en = NAKSHATRA_NAMES["english"][current_nakshatra_index]
        current_nakshatra_name_ml = NAKSHATRA_NAMES["malayalam"][current_nakshatra_index]

        # Calculate transition to next Nakshatra
        next_nakshatra_start_lon = (current_nakshatra_index + 1) * nakshatra_degrees
        remaining_degrees = (next_nakshatra_start_lon - moon_lon) % 360
        remaining_fraction_of_day = remaining_degrees / moon_daily_motion
        next_nakshatra_time = current_time + timedelta(days=remaining_fraction_of_day)

        # Calculate duration in Nazhika
        duration_minutes = (next_nakshatra_time - current_time).total_seconds() / 60
        duration_nazhika = duration_minutes / 24  # 1 Nazhika = 24 minutes

        # Format Nazhika as a mixed fraction
        whole_nazhika = int(duration_nazhika)
        fractional_nazhika = duration_nazhika - whole_nazhika
        fractional_part = Fraction(fractional_nazhika).limit_denominator(12)  # Limit to 1/12

        formatted_nazhika = f"{whole_nazhika} {fractional_part}" if fractional_part else f"{whole_nazhika}"

        # Append results
        results.append({
            "english": current_nakshatra_name_en,
            "malayalam": current_nakshatra_name_ml,
            "start_time": current_time.strftime("%Y-%m-%d %I:%M %p"),
            "end_time": next_nakshatra_time.strftime("%Y-%m-%d %I:%M %p"),
            "nazhika": formatted_nazhika
        })

        # Prepare for the next iteration
        current_time = next_nakshatra_time
        moon_lon = next_nakshatra_start_lon % 360
        current_nakshatra_index = (current_nakshatra_index + 1) % 27

    return results
