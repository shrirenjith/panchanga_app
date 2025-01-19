# core/time_zone_service.py

import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from skyfield.almanac import sunrise_sunset, find_discrete
from skyfield.api import wgs84

logger = logging.getLogger(__name__)

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
            return t.utc_datetime()  # Changed from astimezone to utc_datetime

    return None  # Sunrise not found
