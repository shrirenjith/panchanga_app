import logging
from .ayanamsa import AyanamsaCalculator

logger = logging.getLogger(__name__)

ayanamsa_calculator = AyanamsaCalculator()

class PanchangaCalculator:
    def __init__(self, ephemeris_calculator):
        logger.debug("Initializing PanchangaCalculator")
        if not ephemeris_calculator:
            logger.error("EphemerisCalculator instance is missing")
            raise ValueError("EphemerisCalculator instance is required")
        self.eph_calc = ephemeris_calculator

    def compute_tithi(self, sun_lon, moon_lon):
        """
        Compute Tithi based on the Sun and Moon's sidereal longitudes.
        """
        diff = (moon_lon - sun_lon) % 360
        tithi = int(diff // 12)
        logger.debug(f"Computed Tithi: {tithi} (Sun: {sun_lon}, Moon: {moon_lon})")
        return tithi

    def compute_nakshatra(self, moon_lon):
        """
        Compute Nakshatra based on the Moon's sidereal longitude.
        """
        segment = 360.0 / 27.0
        nakshatra = int((moon_lon % 360) // segment)
        logger.debug(f"Computed Nakshatra: {nakshatra} (Moon: {moon_lon})")
        return nakshatra

    def get_sidereal_positions1(self, utc_time):
        """
        Compute sidereal positions of the Sun and Moon.
        """
        tropical_positions = self.eph_calc.get_tropical_positions(utc_time)
        sun_sidereal = self.get_sidereal_longitude(
            tropical_positions["sun_tropical_longitude"], utc_time.date()
        )
        moon_sidereal = self.get_sidereal_longitude(
            tropical_positions["moon_tropical_longitude"], utc_time.date()
        )
        logger.debug(f"Sidereal Positions: Sun={sun_sidereal}, Moon={moon_sidereal}")
        return {
            "sun_longitude": sun_sidereal,
            "moon_longitude": moon_sidereal
        }

    def get_sidereal_longitude(self, tropical_longitude, date_obj):
        """
        Convert tropical longitude to sidereal longitude using Ayanamsa.
        """
        ayanamsa = ayanamsa_calculator.calculate(date_obj, use_fractional=False)
        sidereal_lon = (tropical_longitude - ayanamsa) % 360
        logger.debug(f"Converted Tropical Longitude {tropical_longitude} to Sidereal {sidereal_lon}")
        return sidereal_lon
