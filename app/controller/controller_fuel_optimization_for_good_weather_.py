
import numpy as np
import pandas as pd
import joblib
from app.validator.validator_fule_optimization_for_good_weather_ import Input
from scipy.optimize import differential_evolution
from datetime import datetime, timedelta
from app.utils.utils_route_fuel_optimization_for_good_weather_ import to_model_required_format ,fuel_consumption_objective


# Load the trained model
model = joblib.load('app/models/orion/fule_optimization_for_good_weather.joblib')
feature_transformer = joblib.load('app/models/orion/feature_transformer.joblib')
target_transformer = joblib.load('app/models/orion/target_transformer.joblib')

async def predict_fuel_consumption(item:Input):
        # adding lag values
    item_dict = to_model_required_format(item)
    
    converted_data = np.array(list(item_dict.values())).reshape(1, -1)
    # Example usage:
    remaining_distance = item_dict["distance_remaining_to_eov"]  # Replace with actual remaining distance
    days_remaining = item_dict["days_remaining"]
    speed_bounds = (8, 20)

# Perform differential evolution optimization
    result = differential_evolution(
    fuel_consumption_objective,
    bounds=[speed_bounds],
    args=(model, target_transformer ,converted_data),
    maxiter=100,
    popsize=10,
    disp=True
    )
    result
    # Extract results
    optimized_speed = result.x[0]
    optimized_fuel_consumption = result.fun

    # Calculate total fuel consumption for the remaining voyage
    total_fuel_consumption = optimized_fuel_consumption * remaining_distance

    # Calculate fuel consumption per day for the remaining days
    fuel_consumption_per_day = total_fuel_consumption / days_remaining if days_remaining != 0 else 0

    # Create a DataFrame for future dates
    today_at_noon = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)

    future_dates = [today_at_noon + timedelta(days=i) for i in range(1, days_remaining + 1)]

    # Create a DataFrame with dates, optimized speed, and fuel consumption per day
    return  pd.DataFrame({
        'Date':  future_dates,
        'Optimized Speed': [optimized_speed] * days_remaining,
        'Fuel Consumption per Day': [fuel_consumption_per_day / 1000] * days_remaining
    }).to_dict('records')
