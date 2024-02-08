from fastapi import APIRouter, Depends ,HTTPException
from app.database_ import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
import numpy as np
import pandas as pd
import joblib
import xmltodict 
from app.validator.validator_fule_optimization_for_good_weather_ import Input
from scipy.optimize import differential_evolution
from datetime import datetime, timedelta
from app.utils.utils_route_fule_optimization_for_good_weather_ import to_model_required_format ,fuel_consumption_objective
from app.controller.controller_fule_optimization_for_good_weather_ import predict_fuel_consumption
router = APIRouter()

# Load the trained model
model = joblib.load('app/models/orion/fule_optimization_for_good_weather.joblib')
feature_transformer = joblib.load('app/models/orion/feature_transformer.joblib')
target_transformer = joblib.load('app/models/orion/target_transformer.joblib')


@router.get("/predict_noon/{vesselid}")
async def predict_fuel_consumptions_from_last_noon(vesselid: int, db=Depends(get_db)):
    query = """
        SELECT
        noonreportdata ->> 'Slip' AS "slip",
        noonreportdata ->> 'ME_RPM' AS "me_rpm",
        noonreportdata ->> 'Distance' AS "distance",
        noonreportdata ->> 'Avg_Speed' AS "avg_speed",
        noonreportdata ->> 'Draft_AFT' AS "draft_aft",
        noonreportdata ->> 'Draft_FWD' AS "draft_fwd",
        noonreportdata ->> 'Sea_Height' AS "sea_height",
        noonreportdata ->> 'Wind_Speed' AS "wind_speed",
        noonreportdata ->> 'Swell_Height' AS "swell_height",
        noonreportdata ->> 'Distance_Remaining_To_EOV' AS "distance_remaining_to_eov",
        noonreportdata ->> 'ME_Running_Hrs' AS "me_running_hrs",
        noonreportdata ->> 'Douglas_Sea_State' AS "douglas_sea_state",
        noonreportdata ->> 'Average_Speed_Since_SOV' AS "average_speed_since_sov",
        noonreportdata ->> 'Distance_Covered_Since_SOV' AS "distance_covered_since_sov",
        noonreportdata ->> 'Total_HFO_Consumed_In_MT' AS "total_hfo_consumed_in_mt",
        noonreportdata ->> 'ETA_Next_Port' AS "eta_next_port",
        noonreportdata ->> 'Total_HFOME_Consumed_In_MT' AS "total_hfome_consumed_in_mt",
        noonreportdata ->> 'Total_ULSGOME_Consumed_In_MT' AS "total_ulsgome_consumed_in_mt",
        noonreportdata ->> 'Total_VLSFOME_Consumed_In_MT' AS "total_vlsfome_consumed_in_mt",
        noonreportdata ->> 'Total_VLSGOME_Consumed_In_MT' AS "total_vlsgome_consumed_in_mt"
    FROM (
        SELECT *,
            row_number() OVER (ORDER BY id DESC) as rn
        FROM shipping_db.enoonreporttable
        WHERE vesselid = $1
    ) AS subquery
    WHERE rn = 2;
    """
    result = await db.fetch(query, vesselid)
    if result:
        # Convert the asyncpg.Record to a standard Python dictionary
        record_dict = dict(result[0])
        
        prediction = await predict_fuel_consumption(record_dict)
        
        return prediction
    else:
        return {"error": "No data found for vessel ID {}".format(vesselid)}

@router.post("/predict_noon")
async def predict_noon(item: Input):
    return await predict_fuel_consumption(item)
    