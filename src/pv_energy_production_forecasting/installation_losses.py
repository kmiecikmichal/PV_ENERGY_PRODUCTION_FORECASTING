

# Function to get photovoltaic cell temperature based on forecasts of temperature and irradiance
# @params:  installation - installation object from class Installation
#           temp_dict - dict with temperature (values) and datetime (keys)
#           solar_irradiance_dict - dict with solar irradiance (values) and datetime (keys)
def get_pv_cell_temperature(installation, temp_dict, solar_irradiance_dict):
    # Parameters to formula using NOCT values
    temp_pv_cell_noct = installation.pv_cell_temp_noct
    temp_ambient_noct = 20.0  # Celsius degrees
    solar_irradiance_noct = 800  # [W/m^2]
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


# Function to get temperature losses of pv installation in [%]
# @params:  installation - installation object from class Installation
#           pv_cell_temp_dict - dict with temperature of pv cell (values) and datetime (keys)
def get_temperature_losses(installation, pv_cell_temp_dict):
    # Parameter to formula
    temp_coeff_of_power = installation.temp_coeff_of_power
    temp_stc = 25  # Celsius degrees
    # temperature losses dict
    temp_losses_dict = {}
    for date_time in pv_cell_temp_dict:
        pv_cell_temp = pv_cell_temp_dict[date_time]
        temp_difference = pv_cell_temp - temp_stc
        # Temp losses formula. We use "* -1" because this linear function is descending (negative temp_coeff of power)
        # and we need a positive value of total temperature losses
        temp_losses = temp_difference * temp_coeff_of_power * -1
        temp_losses_dict[date_time] = temp_losses

    return temp_losses_dict


def temperature_losses_linear_formula():
    pass