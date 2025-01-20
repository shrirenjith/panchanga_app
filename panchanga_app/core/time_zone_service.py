# core/time_zone_service.py

import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from skyfield.almanac import sunrise_sunset, find_discrete
from skyfield.api import wgs84
from timezonefinder import TimezoneFinder

logger = logging.getLogger(__name__)
tf = TimezoneFinder()

def get_timezone_from_lat_lon(lat, lon):
    """Get timezone string from latitude and longitude."""
    return tf.timezone_at(lat=lat, lng=lon)

def get_local_sunrise(calculator, local_date, lat, lon):
    """
    Compute local sunrise for a given date and location.
    """
    logger.debug(f"Computing sunrise for date: {local_date}, lat: {lat}, lon: {lon}")
    
    # Get the ephemeris calculator from the panchanga calculator
    ts = calculator.eph_calc.ts
    eph = calculator.eph_calc.eph
    location = wgs84.latlon(lat, lon)

    # Define the time range for finding sunrise
    start_utc = datetime(local_date.year, local_date.month, local_date.day, tzinfo=ZoneInfo("UTC"))
    end_utc = start_utc + timedelta(days=1)

    # Compute sunrise using Skyfield's utilities
    f = sunrise_sunset(eph, location)
    t0 = ts.from_datetime(start_utc)
    t1 = ts.from_datetime(end_utc)

    times, events = find_discrete(t0, t1, f)
    for t, event in zip(times, events):
        if event == 1:  # Sunrise event
            sunrise_utc = t.utc_datetime()
            logger.debug(f"Sunrise in UTC: {sunrise_utc}")
            
            # Convert to local time using the location's timezone
            local_timezone = ZoneInfo(get_timezone_from_lat_lon(lat, lon))
            sunrise_local = sunrise_utc.astimezone(local_timezone)
            logger.debug(f"Sunrise in local time: {sunrise_local}")
            return sunrise_local

    logger.warning(f"No sunrise found for date: {local_date}, lat: {lat}, lon: {lon}")
    return None  # Sunrise not found
