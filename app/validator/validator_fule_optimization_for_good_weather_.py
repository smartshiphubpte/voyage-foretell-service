from pydantic import BaseModel, Field

class Input(BaseModel):
    slip: float
    me_rpm: float
    distance: float
    avg_speed: float
    draft_aft: float
    draft_fwd: float
    sea_height: float
    wind_speed: float
    swell_height: float
    distance_remaining_to_eov: float
    me_running_hrs: float
    douglas_sea_state: float
    average_speed_since_sov: float
    distance_covered_since_sov: float
    total_hfo_consumed_in_mt: float
    # total_fuel_consumption_mt: int = Field(..., alias="Total Fuel Consumption(MT)")
    # main_draft_mtr: float = Field(..., alias="Main Draft (mtr)")
    # trim_mtr: float = Field(..., alias="Trim(mtr)")
    # shaft_power: float
    # me_power: float
    eta_next_port: str
    total_hfome_consumed_in_mt: float
    total_ulsgome_consumed_in_mt: float
    total_vlsfome_consumed_in_mt: float
    total_vlsgome_consumed_in_mt: float

    class Config:
        allow_population_by_field_name = True
