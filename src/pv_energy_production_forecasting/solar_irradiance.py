import numpy as np
from solarpy import irradiance_on_plane


# Function to return get solar irradiance in [W/m^2]
# Only datetime from clouds_dict will be used
# @params:  installation - installation object from class Installation
#           clouds_dict - dict with datetime and clouds forecast from get_hourly_forecast function
def solar_irradiance(installation, clouds_dict):
    # Plane pointing zenith
    v_norm = np.array([0, 0, -1])
    # Installation parameters
    above_sea_level = installation.above_sea_level
    latitude = installation.latitude
    # Solar Irradiance dict
    solar_irradiance_dict = {}
    # For every element in clouds dict
    for date_time in clouds_dict:
        # Computed solar irradiance
        irradiance = irradiance_on_plane(v_norm, above_sea_level, date_time, latitude)
        # Dict_name[key] = value
        solar_irradiance_dict[date_time] = irradiance

    return solar_irradiance_dict
