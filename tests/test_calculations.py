import pytest
from datetime import datetime

def test_compute_tithi(panchanga_calculator):
    # Test with known values
    sun_lon = 0
    moon_lon = 12  # 12 degrees apart = Tithi 1
    tithi = panchanga_calculator.compute_tithi(sun_lon, moon_lon)
    assert tithi == 1

def test_compute_nakshatra(panchanga_calculator):
    # Test with known values
    moon_lon = 13.333  # Should be Nakshatra 1
    nakshatra = panchanga_calculator.compute_nakshatra(moon_lon)
    assert nakshatra == 1

def test_get_sidereal_positions(panchanga_calculator, sample_datetime):
    positions = panchanga_calculator.get_sidereal_positions1(sample_datetime)
    assert "sun_longitude" in positions
    assert "moon_longitude" in positions
    assert 0 <= positions["sun_longitude"] < 360
    assert 0 <= positions["moon_longitude"] < 360 