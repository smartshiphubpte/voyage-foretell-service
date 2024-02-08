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
        CAST(noonreportdata ->> 'Slip' AS FLOAT) AS "slip",
        CAST(noonreportdata ->> 'ME_RPM' AS FLOAT) AS "me_rpm",
        CAST(noonreportdata ->> 'Distance' AS FLOAT) AS "distance",
        CAST(noonreportdata ->> 'Avg_Speed' AS FLOAT) AS "avg_speed",
        CAST(noonreportdata ->> 'Draft_AFT' AS FLOAT) AS "draft_aft",
        CAST(noonreportdata ->> 'Draft_FWD' AS FLOAT) AS "draft_fwd",
        CAST(noonreportdata ->> 'Sea_Height' AS FLOAT) AS "sea_height",
        CAST(noonreportdata ->> 'Wind_Speed' AS FLOAT) AS "wind_speed",
        CAST(noonreportdata ->> 'Swell_Height' AS FLOAT) AS "swell_height",
        CAST(noonreportdata ->> 'Distance_Remaining_To_EOV' AS FLOAT) AS "distance_remaining_to_eov",
        CAST(noonreportdata ->> 'ME_Running_Hrs' AS FLOAT) AS "me_running_hrs",
        CAST(noonreportdata ->> 'Douglas_Sea_State' AS FLOAT) AS "douglas_sea_state",
        CAST(noonreportdata ->> 'Average_Speed_Since_SOV' AS FLOAT) AS "average_speed_since_sov",
        CAST(noonreportdata ->> 'Distance_Covered_Since_SOV' AS FLOAT) AS "distance_covered_since_sov",
        CAST(noonreportdata ->> 'Total_HFO_Consumed_In_MT' AS FLOAT) AS "total_hfo_consumed_in_mt",
        noonreportdata ->> 'ETA_Next_Port' AS "eta_next_port",
        CAST(noonreportdata ->> 'Total_HFOME_Consumed_In_MT' AS FLOAT) AS "total_hfome_consumed_in_mt",
        CAST(noonreportdata ->> 'Total_ULSGOME_Consumed_In_MT' AS FLOAT) AS "total_ulsgome_consumed_in_mt",
        CAST(noonreportdata ->> 'Total_VLSFOME_Consumed_In_MT' AS FLOAT) AS "total_vlsfome_consumed_in_mt",
        CAST(noonreportdata ->> 'Total_VLSGOME_Consumed_In_MT' AS FLOAT) AS "total_vlsgome_consumed_in_mt"
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
    return await predict_fuel_consumption(item.model_dump())
    