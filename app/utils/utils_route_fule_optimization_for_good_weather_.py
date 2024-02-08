from datetime import datetime, timedelta
import numpy as np

def to_model_required_format(noon_dict):
    # noon_dict = noon_report.model_dump() 
    # added lag values means given by prashant sir 
    noon_dict["Total Fuel Consumption(MT)_lag_3"] = 20.179280575539565
    noon_dict["me_rpm_lag_3"] = 70.39496402877698 
    noon_dict["avg_speed_lag_3"] = 12.241079136690646
    noon_dict["me_power_lag_3"] = 4637.99019391367

    # added power values means given by prashant sir 
    noon_dict["me_power"] = 4637.99019391367
    noon_dict["shaft_power"] = 4037.99019391367
    noon_dict["days_remaining"] = (datetime.strptime(noon_dict['eta_next_port'], "%d %b %Y %H%M") - datetime.now()).days
    noon_dict.pop("eta_next_port")

    # calculate total fuel consumption
    calculate_total_fuel_consumption(noon_dict)
    # calculate MEFC 
    calculate_MEFC(noon_dict)
    # calculate main draft 
    calculate_main_draft_and_trim(noon_dict)

    return noon_dict



def fuel_consumption_objective(speed, *args):
    model = args[0]
    target_transformer_filename = args[1]
    input_data_transformed = args[2] 
    # Predict transformed fuel consumption
    predicted_transformed = model.predict(input_data_transformed)
    # Inverse transform the predicted value back to the original scale
    predicted_original = target_transformer_filename.inverse_transform(predicted_transformed)

    return predicted_original[0, 0]

def calculate_total_fuel_consumption(noon_dict):
    noon_dict["Total Fuel Consumption(MT)"] =  float(noon_dict["total_hfome_consumed_in_mt"]) + float(noon_dict["total_ulsgome_consumed_in_mt"]) + float(noon_dict["total_vlsfome_consumed_in_mt"]) + float(noon_dict["total_vlsgome_consumed_in_mt"])

    noon_dict.pop("total_hfome_consumed_in_mt")
    noon_dict.pop("total_ulsgome_consumed_in_mt")
    noon_dict.pop("total_vlsfome_consumed_in_mt")
    noon_dict.pop("total_vlsgome_consumed_in_mt")
    return noon_dict

def calculate_MEFC(noon_dict):
    noon_dict["MECF"] = (float(noon_dict["Total Fuel Consumption(MT)"]) / float(noon_dict['me_running_hrs'])) * 24
    return noon_dict
    
def calculate_main_draft_and_trim(noon_dict):
    # noon_dict["Main Draft (mtr)"] = (float(noon_dict['draft_aft']) + float(noon_dict['draft_fwd'] / 2))
    noon_dict["Main Draft (mtr)"] = (float(noon_dict['draft_aft']) + float(noon_dict['draft_fwd'] )/2)
    noon_dict["Trim(mtr)"] = float(noon_dict['draft_aft']) - float(noon_dict['draft_fwd']) 
    return noon_dict