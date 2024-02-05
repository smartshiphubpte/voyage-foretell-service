from pydantic import BaseModel, Field

class Input(BaseModel):
    slip: float
    me_rpm: int
    distance: float
    avg_speed: float
    draft_aft: float
    draft_fwd: float
    sea_height: float
    wind_speed: int
    swell_height: float
    distance_remaining_to_eov: float
    me_running_hrs: int
    douglas_sea_state: int
    average_speed_since_sov: float
    distance_covered_since_sov: float
    total_hfo_consumed_in_mt: int
    total_fuel_consumption_mt: int = Field(..., alias="Total Fuel Consumption(MT)")
    mecf: float = Field(..., alias="MECF")
    main_draft_mtr: float = Field(..., alias="Main Draft (mtr)")
    trim_mtr: float = Field(..., alias="Trim(mtr)")
    shaft_power: int
    me_power: int
    days_remaining: int
    total_fuel_consumption_mt_lag_3: int = Field(..., alias="Total Fuel Consumption(MT)_lag_3")
    me_rpm_lag_3: int
    avg_speed_lag_3: float
    me_power_lag_3: int

    class Config:
        allow_population_by_field_name = True
