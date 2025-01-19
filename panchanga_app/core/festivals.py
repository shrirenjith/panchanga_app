# panchanga_app/core/festivals.py

from typing import List, Dict

FESTIVALS = [
    {
        "name": "Vishu",
        "type": "solar_entry",
        "zodiac_start_degree": 0,  # Aries starts at 0°, triggers Vishu
    },
    {
        "name": "Onam (Thiruvonam Day)",
        "type": "month_nakshatra",
        "month_name": "Chingam",       # for example
        "nakshatra_index": 22,        # if 22 corresponds to Thiruvonam in your indexing
    },
    # ... Add more as needed
]

def check_festivals(
    malayalam_month: str,
    nakshatra_index: int,
    sun_longitude: float
) -> List[str]:
    """
    Returns a list of festivals that match the given Panchāṅga data.
    """
    matched = []
    for fest in FESTIVALS:
        if fest["type"] == "solar_entry":
            # Example: Vishu => sun_longitude near 0° Aries
            # This might require checking if the Sun *crosses* 0° on this day
            # For demonstration, let's say if it's 0° ± 1°:
            if abs(sun_longitude - fest["zodiac_start_degree"]) < 1:
                matched.append(fest["name"])

        elif fest["type"] == "month_nakshatra":
            if fest["month_name"] == malayalam_month and fest["nakshatra_index"] == nakshatra_index:
                matched.append(fest["name"])

    return matched
