import logging
from skyfield.api import load
from skyfield.almanac import sunrise_sunset, find_discrete
from skyfield.framelib import ecliptic_frame
from skyfield.api import wgs84

logger = logging.getLogger(__name__)

class EphemerisCalculator:
    def __init__(self, ephemeris_file='de421.bsp'):
        """
        Initialize the EphemerisCalculator with ephemeris data.
        """
        logger.debug(f"Initializing EphemerisCalculator with file: {ephemeris_file}")
        self.ts = load.timescale()
        self.eph = load(ephemeris_file)

    def get_tropical_positions(self, utc_time):
        """
        Calculate tropical positions of the Sun and Moon.
        """
        logger.debug(f"Calculating tropical positions for UTC time: {utc_time}")
        t = self.ts.from_datetime(utc_time)

        # Sun's tropical longitude
        sun = self.eph['Sun']
        sun_position = self.eph['Earth'].at(t).observe(sun).apparent()
        sun_latlon = sun_position.frame_latlon(ecliptic_frame)
        sun_tropical_lon = sun_latlon[1].degrees

        # Moon's tropical longitude
        moon = self.eph['Moon']
        moon_position = self.eph['Earth'].at(t).observe(moon).apparent()
        moon_latlon = moon_position.frame_latlon(ecliptic_frame)
        moon_tropical_lon = moon_latlon[1].degrees

        logger.debug(f"Sun Longitude: {sun_tropical_lon}, Moon Longitude: {moon_tropical_lon}")

        return {
            "sun_tropical_longitude": sun_tropical_lon,
            "moon_tropical_longitude": moon_tropical_lon
        }

    def find_sunrise_utc(self, lat, lon, start_utc, end_utc):
        """
        Compute sunrise time in UTC for the given lat/lon and time range.
        """
        logger.debug(f"Finding sunrise for lat={lat}, lon={lon}, start={start_utc}, end={end_utc}")
        location = wgs84.latlon(latitude_degrees=lat, longitude_degrees=lon)
        f = sunrise_sunset(self.eph, location)

        t0 = self.ts.from_datetime(start_utc)
        t1 = self.ts.from_datetime(end_utc)

        times, events = find_discrete(t0, t1, f)
        for t, event in zip(times, events):
            if event == 1:  # Sunrise event
                logger.debug(f"Sunrise found at: {t.utc_datetime()}")
                return t.utc_datetime()

        logger.warning("No sunrise found in the given range.")
        return None
