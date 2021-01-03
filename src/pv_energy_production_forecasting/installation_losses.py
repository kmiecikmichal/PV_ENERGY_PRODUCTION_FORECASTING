import math
import sys


# Function to get pv installation efficiency (normalized)
# @params:  installation - installation object from class Installation
#           temp_dict - dict with temperature (values) and datetime (keys)
#           solar_irradiance_dict - dict with solar irradiance (values) and datetime (keys)
def get_installation_efficiency(installation, temp_dict, solar_irradiance_dict):
    # Pv cell temperature dict
    pv_cell_temp_dict = get_pv_cell_temperature(installation, temp_dict, solar_irradiance_dict)
    # Temperature and irradiance losses normalized
    temp_irr_efficiency_dict = get_temperature_and_irradiance_efficiency(installation, pv_cell_temp_dict, solar_irradiance_dict)
    # Some estimated constant losses
    cables_loss = 0.01
    inverter_loss = 0.025
    total_constant_loss = cables_loss + inverter_loss
    # Installation efficiency dict
    inst_efficiency_dict = {}
    for date_time in temp_irr_efficiency_dict:
        temp_irr_efficiency = temp_irr_efficiency_dict[date_time]
        inst_efficiency = temp_irr_efficiency * (1 - total_constant_loss)
        inst_efficiency_dict[date_time] = inst_efficiency

    return inst_efficiency_dict


# Function to get temperature and irradiance efficiency in pv installation
# @params:  installation - installation object from class Installation
#           pv_cell_temp_dict - dict with temperature of pv cell (values) and datetime (keys)
#           solar_irradiance_dict - dict with solar irradiance (values) and datetime (keys)
def get_temperature_and_irradiance_efficiency(installation, pv_cell_temp_dict, solar_irradiance_dict):
    # Dicts with Parameters to formula
    i_sc_dict = get_short_circuit_current(installation, pv_cell_temp_dict, solar_irradiance_dict)
    v_oc_dict = get_open_circuit_voltage(installation, pv_cell_temp_dict, solar_irradiance_dict)
    fill_factor_dict = get_fill_factor(v_oc_dict, pv_cell_temp_dict)
    # And constant parameters to formula
    i_sc_stc = installation.short_circuit_current  # Short Circuit Current STC from database
    v_oc_stc = installation.open_circuit_voltage  # Open Circuit Voltage STC from database
    cell_power_stc = installation.nominal_cell_power  # Nominal Cell Power STC from datebase
    # Temperature and irradiance dict
    temp_irr_efficiency_dict = {}
    for date_time in i_sc_dict:
        # Extract parameters to formula from dict
        i_sc = i_sc_dict[date_time]
        v_oc = v_oc_dict[date_time]
        fill_factor = fill_factor_dict[date_time]
        # Forecasted Cell Power
        cell_power = i_sc * v_oc * fill_factor
        # Cell Power Ratio
        cell_power_ratio = cell_power / cell_power_stc
        # Temperature and irradiance losses (normalized)
        temp_irr_efficiency_dict[date_time] = cell_power_ratio

    return temp_irr_efficiency_dict


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
        pv_cell_temp = temp_ambient + (temp_pv_cell_noct - temp_ambient_noct) * (
                    solar_irradiance / solar_irradiance_noct)
        # Packing to dict
        pv_cell_temp_dict[date_time] = pv_cell_temp

    return pv_cell_temp_dict


# Function to get forecasted Isc - Short Circuit Current
# @params:  installation - installation object from class Installation
#           pv_cell_temp_dict - dict with temperature of pv cell (values) and datetime (keys)
#           solar_irradiance_dict - dict with solar irradiance (values) and datetime (keys)
def get_short_circuit_current(installation, pv_cell_temp_dict, solar_irradiance_dict):
    # Parameters to formula
    i_sc_stc = installation.short_circuit_current  # Short Circuit Current STC from database
    temp_coeff_of_current = installation.temp_coeff_of_current  # Temperature coefficient of current
    irradiance_stc = 1000  # Irradiance STC = 1000 W/m^2
    temp_stc = 25  # Temperature STC = 25 deg.C
    # Short Circuit Current dict
    i_sc_dict = {}
    for date_time in pv_cell_temp_dict:
        pv_cell_temp = pv_cell_temp_dict[date_time]  # Pv cell temperature
        temp_difference = pv_cell_temp - temp_stc
        irradiance = solar_irradiance_dict[date_time]
        i_sc = i_sc_stc * (1 + (temp_coeff_of_current / 100) * temp_difference) * (irradiance / irradiance_stc)
        i_sc_dict[date_time] = i_sc

    return i_sc_dict


# Function to get forecasted Uoc - Open Circuit Voltage
# @params:  installation - installation object from class Installation
#           pv_cell_temp_dict - dict with temperature of pv cell (values) and datetime (keys)
#           solar_irradiance_dict - dict with solar irradiance (values) and datetime (keys)
def get_open_circuit_voltage(installation, pv_cell_temp_dict, solar_irradiance_dict):
    # Parameters to formula
    v_oc_stc = installation.open_circuit_voltage  # Open Circuit Voltage STC from database
    temp_coeff_of_voltage = installation.temp_coeff_of_voltage  # Temperature coefficient of voltage
    irr_corr_factor = 0.06  # Irradiance Correction Factor
    irradiance_stc = 1000  # Irradiance STC = 1000 W/m^2
    temp_stc = 25  # Temperature STC = 25 deg.C
    # Open Circuit Voltage dict
    v_oc_dict = {}
    for date_time in pv_cell_temp_dict:
        pv_cell_temp = pv_cell_temp_dict[date_time]  # Pv cell temperature
        temp_difference = pv_cell_temp - temp_stc
        irradiance = solar_irradiance_dict[date_time]
        # If statement to avoid log(0) when forecasted irradiance at night = 0 w/m^2
        if irradiance / irradiance_stc > 0:
            v_oc = v_oc_stc * (1 + ((temp_coeff_of_voltage / 100) * temp_difference) + irr_corr_factor
                               * math.log(irradiance / irradiance_stc))
            # Because extremely small numbers can cause big issues inside logarithm function,
            # for example negative values of v_oc
            if v_oc < 0:
                v_oc = 0
        else:
            v_oc = 0.0

        v_oc_dict[date_time] = v_oc

    return v_oc_dict


# Function to get forecasted fill factor of pv installation
# @params:  v_oc_dict - dict with open circuit voltage forecasts
#           pv_cell_temp_dict - dict with temperature of pv cell (values) and datetime (keys)
def get_fill_factor(v_oc_dict, pv_cell_temp_dict):
    # Parameters to calculate normalized Voc
    q = 1.6 * 10 ** -19  # Elementary charge
    k = 1.38 * 10 ** -23  # Boltzmann's constant
    n = 1  # Ideality factor
    # Fill factor dict
    fill_factor_dict = {}
    for date_time in pv_cell_temp_dict:
        v_oc = v_oc_dict[date_time]
        # Another parameter to calculate normalized Voc
        cell_temp = pv_cell_temp_dict[date_time]  # Cell temperature in Celsius deg.
        cell_temp_kelvin = cell_temp + 273.15  # Cell temperature in Kelvins
        # Normalized Voc
        v_oc_norm = (q / (n * k * cell_temp_kelvin)) * v_oc
        # Fill Factor
        if v_oc_norm + 0.72 > 0:
            fill_factor = (v_oc_norm - math.log(v_oc_norm + 0.72)) / (v_oc_norm + 1)
            fill_factor_dict[date_time] = fill_factor
        else:
            print("ERROR: get_fill_factor function, the logarithmic number is not greater than 0")
            sys.exit(1)

    return fill_factor_dict
