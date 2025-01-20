from pydantic import BaseModel, Field
from datetime import date
from typing import List, Dict, Optional

class PanchangaRequest(BaseModel):
    latitude: Optional[float] = Field(None, description="GPS latitude (default: Thrissur)")
    longitude: Optional[float] = Field(None, description="GPS longitude (default: Thrissur)")
    local_date: date = Field(..., description="Local date for calculations (YYYY-MM-DD)")

class MalayalamDate(BaseModel):
    month_name: str
    month_day: int
    year: int

class NakshatraDetails(BaseModel):
    english: str = Field(..., description="Nakshatra name in English")
    malayalam: str = Field(..., description="Nakshatra name in Malayalam")
    start_time: str = Field(..., description="Start time of the Nakshatra in HH:MM AM/PM format")
    end_time: str = Field(..., description="End time of the Nakshatra in HH:MM AM/PM format")
    nazhika: str = Field(..., description="Nazhika representation of the duration")

class PanchangaResponse(BaseModel):
    sunrise_local: str = Field(..., description="Local sunrise time in ISO format")
    tithi_index: int
    festivals: List[str]
    malayalam_date: MalayalamDate
    tithi_name: Dict[str, str]
    nakshatra: List[NakshatraDetails]
