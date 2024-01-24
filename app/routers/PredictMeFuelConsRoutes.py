from fastapi import APIRouter

router = APIRouter()

@router.get("/predict")
async def predict_fuel_consumption():
    return {"message": "Predicting Fuel Consumption..."}
