

# Function to get photovoltaic cell temperature based on forecasts of temperature and irradiance
# @params:  installation - installation object from class Installation
#           temp_dict - dict with temperature (values) and datetime (keys)
#           solar_irradiance_dict - dict with solar irradiance (values) and datetime (keys)
def get_pv_cell_temperature(installation, temp_dict, solar_irradiance_dict):
    # Parameters to formula using NOCT values
    temp_pv_cell_noct = installation.pv_cell_temp_noct
    temp_ambient_noct = 20.0  # Celsius degrees
    solar_irradiance_noct = 800  # W/M^2
    # pv cell temperature dict
    pv_cell_temp_dict = {}
    for date_time in temp_dict:
        # Forecast parameters
        temp_ambient = temp_dict[date_time]
        solar_irradiance = solar_irradiance_dict[date_time]
        # Calculations
        pv_cell_temp = temp_ambient + (temp_pv_cell_noct - temp_ambient_noct) * (solar_irradiance / solar_irradiance_noct)
        # Packing to dict
        pv_cell_temp_dict[date_time] = pv_cell_temp

    return pv_cell_temp_dict
