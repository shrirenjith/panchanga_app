import pytest
from datetime import datetime, date
from panchanga_app.core.ephemeris import EphemerisCalculator
from panchanga_app.core.calculations import PanchangaCalculator

@pytest.fixture
def ephemeris_calculator():
    return EphemerisCalculator()

@pytest.fixture
def panchanga_calculator(ephemeris_calculator):
    return PanchangaCalculator(ephemeris_calculator)

@pytest.fixture
def sample_date():
    return date(2024, 1, 1)

@pytest.fixture
def sample_datetime():
    return datetime(2024, 1, 1, 12, 0) 