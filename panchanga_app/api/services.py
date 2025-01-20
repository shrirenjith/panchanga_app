from datetime import date
from zoneinfo import ZoneInfo
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from ..core.festivals import check_festivals
from ..core.time_zone_service import get_local_sunrise
from ..core.nakshatra import get_tithi_name, get_nakshatra_name, calculate_nakshatra_timings
from ..core.malayalam_calendar import get_malayalam_date

def get_panchanga_data(calculator, lat: float, lon: float, local_date: date):
    logger.debug(f"Starting Panchanga data computation for lat={lat}, lon={lon}, date={local_date}")
    logger.debug(f"Calculator type: {type(calculator)}")
    try:
        sunrise_local = get_local_sunrise(calculator, local_date, lat, lon)
        if not sunrise_local:
            logger.error("Failed to compute local sunrise")
            raise ValueError("Failed to compute local sunrise")

        logger.debug(f"Local sunrise: {sunrise_local}")

        sunrise_utc = sunrise_local.astimezone(ZoneInfo("UTC"))
        logger.debug(f"Sunrise UTC: {sunrise_utc}")

        sidereal_positions = calculator.get_sidereal_positions1(sunrise_utc)
        logger.debug(f"Sidereal positions: {sidereal_positions}")

        tithi_idx = calculator.compute_tithi(sidereal_positions["sun_longitude"], sidereal_positions["moon_longitude"])
        nakshatra_idx = calculator.compute_nakshatra(sidereal_positions["moon_longitude"])
        logger.debug(f"Tithi index: {tithi_idx}, Nakshatra index: {nakshatra_idx}")

        tithi_name = {
            "english": get_tithi_name(tithi_idx, "english"),
            "malayalam": get_tithi_name(tithi_idx, "malayalam")
        }
        nakshatra_name = {
            "english": get_nakshatra_name(nakshatra_idx, "english"),
            "malayalam": get_nakshatra_name(nakshatra_idx, "malayalam")
        }
        logger.debug(f"Tithi name: {tithi_name}, Nakshatra name: {nakshatra_name}")

        malayalam_date = get_malayalam_date(calculator, sunrise_local, lat, lon)
        logger.debug(f"Malayalam date: {malayalam_date}")
# Calculate Nakshatra timings
        nakshatra_timings = calculate_nakshatra_timings(
            moon_lon=sidereal_positions["moon_longitude"],
            sunrise_local=sunrise_local,
            eph_calc=calculator.eph_calc
        )

        # Get the festivals for the given date
        festivals_today = check_festivals(
            malayalam_date["month_name"], nakshatra_idx, sidereal_positions["sun_longitude"]
        )
        logger.debug(f"Festivals today: {festivals_today}")

        return {
            "sunrise_local": sunrise_local.isoformat(),
            "tithi_index": tithi_idx,
            "tithi_name": tithi_name,
            "nakshatra_index": nakshatra_idx,
            "nakshatra":  nakshatra_timings,
            "malayalam_date": {
                "month_name": malayalam_date["month_name"],
                "month_day": malayalam_date["month_day"],
                "year": malayalam_date["year"]
            },
            "festivals": festivals_today
        }

    except Exception as e:
        logger.error(f"Error in get_panchanga_data: {e}")
        return {
            "sunrise_local": None,
            "error": str(e)
        }
