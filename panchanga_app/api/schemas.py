# panchanga_app/api/schemas.py

from pydantic import BaseModel, Field
from datetime import date
from typing import List, Dict

class PanchangaRequest(BaseModel):
    latitude: float = Field(..., description="GPS latitude")
    longitude: float = Field(..., description="GPS longitude")
    local_date: date = Field(..., description="Local date for calculations (YYYY-MM-DD)")

class MalayalamDate(BaseModel):
    month_name: str
    month_day: int
    year: int

class PanchangaResponse(BaseModel):
    sunrise_local: str = Field(..., description="Local sunrise time in ISO format")
    tithi_index: int
    nakshatra_index: int
    festivals: List[str]
    malayalam_date: MalayalamDate
    tithi_name: Dict[str, str]
    nakshatra_name: Dict[str, str]
