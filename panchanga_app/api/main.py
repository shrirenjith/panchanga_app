from fastapi import FastAPI, Depends, HTTPException
from panchanga_app.api.schemas import PanchangaRequest, PanchangaResponse
from panchanga_app.api.services import get_panchanga_data
from panchanga_app.core.calculations import PanchangaCalculator
from panchanga_app.core.ephemeris import EphemerisCalculator
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
# Default coordinates for Thrissur, Kerala
DEFAULT_LATITUDE = 10.5276
DEFAULT_LONGITUDE = 76.2144

def get_ephemeris_calculator():
    logger.debug("Creating EphemerisCalculator instance")
    return EphemerisCalculator()

def get_panchanga_calculator(
    ephemeris_calculator: EphemerisCalculator = Depends(get_ephemeris_calculator)
):
    logger.debug("Creating PanchangaCalculator instance")
    return PanchangaCalculator(ephemeris_calculator)

@app.post("/panchanga", response_model=PanchangaResponse)
def compute_panchanga(
    req: PanchangaRequest,
    calculator: PanchangaCalculator = Depends(get_panchanga_calculator)
):
    logger.debug(f"Received request: {req}")
    try:
        # Use default coordinates if not provided
        latitude = req.latitude or DEFAULT_LATITUDE
        longitude = req.longitude or DEFAULT_LONGITUDE

        result = get_panchanga_data(
            calculator=calculator,
            lat=latitude,
            lon=longitude,
            local_date=req.local_date
        )
        logger.debug(f"Computed Panchanga data: {result}")
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result

    except Exception as e:
        logger.error(f"Error in compute_panchanga: {e}")
        raise HTTPException(status_code=500, detail=str(e))
