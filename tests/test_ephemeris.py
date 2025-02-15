import pytest
from datetime import datetime, timedelta

@pytest.fixture
def sample_datetime():
    return datetime(2024, 1, 1, 12, 0, 0)  # Noon on Jan 1, 2024

def test_get_tropical_positions(ephemeris_calculator, sample_datetime):
    positions = ephemeris_calculator.get_tropical_positions(sample_datetime)
    assert "sun_tropical_longitude" in positions
    assert "moon_tropical_longitude" in positions
    assert 0 <= positions["sun_tropical_longitude"] < 360
    assert 0 <= positions["moon_tropical_longitude"] < 360

def test_find_sunrise_utc(ephemeris_calculator):
    # Test for Thrissur, Kerala
    lat, lon = 10.5276, 76.2144
    start_time = datetime(2024, 1, 1)
    end_time = start_time + timedelta(days=1)
    
    sunrise = ephemeris_calculator.find_sunrise_utc(
        lat, lon, start_time, end_time
    )
    
    assert sunrise is not None
    assert isinstance(sunrise, datetime) 