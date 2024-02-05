from fastapi import APIRouter, Depends
from app.database_ import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
import numpy as np
import joblib
from app.validator.validator_fule_optimization_for_good_weather_ import Input

router = APIRouter()

# Load the trained model
model = joblib.load('app/models/orion/fule_optimization_for_good_weather.joblib')


@router.get("/predict")
async def predict_fuel_consumption(db: AsyncSession = Depends(get_db)):
    return  (await db.execute(text("SELECT * FROM shipping_db.user"))).fetchall()

@router.post("/predict_noon")
async def predict_noon(item: Input):
    prediction = model.predict(item)
    return {"class": prediction}