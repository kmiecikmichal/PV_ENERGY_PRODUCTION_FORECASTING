import numpy as np
import math
from solarpy import irradiance_on_plane
from pyephem_sunpath.sunpath import sunpos


# Function to return a solar irradiance in [W/m^2]
# @params:  installation - installation object from class Installation
#           clouds_dict - dict with datetime and clouds forecast from get_hourly_forecast function
def get_solar_irradiance(installation, clouds_dict):
    # Parameters to formula
    a_coefficient = 0.25
    # Get clear sky irradiance
    clear_sky_irradiance_dict = get_clear_sky_solar_irradiance(installation, clouds_dict)
    # Get relative insolation dict
    relative_insolation_dict = get_relative_insolation(clouds_dict)
    # Solar irradiance dict
    solar_irradiance_dict = {}
    # For every element in clouds dict
    for date_time in clear_sky_irradiance_dict:
        clear_sky_irradiance = clear_sky_irradiance_dict[date_time]
        # It's not the safest solution to use first dict's keys to manage second dict, but they have identical keys
        relative_insolation = relative_insolation_dict[date_time]
        solar_irradiance = clear_sky_irradiance * (a_coefficient + ((1 - a_coefficient) * relative_insolation))
        solar_irradiance_dict[date_time] = solar_irradiance

    return solar_irradiance_dict


# Function to return a clear sky solar irradiance in [W/m^2]
# @params:  installation - installation object from class Installation
#           clouds_dict - dict with datetime and clouds forecast from get_hourly_forecast function
def get_clear_sky_solar_irradiance(installation, clouds_dict):
    # Get horizontal solar irradiation dict
    horizontal_solar_irradiance_dict = get_horizontal_solar_irradiance(installation, clouds_dict)
    # Get sun position dict necessary to get correction factor
    sun_position_dict = get_sun_position(installation, clouds_dict)
    # Get correction factor dict
    correction_factor_dict = get_correction_factor(installation, sun_position_dict)
    # Solar Irradiance dict- as a key- datetime, as a value- solar irradiance
    solar_irradiance_dict = {}
    # For every element in horizontal solar irradiance dict
    for date_time in horizontal_solar_irradiance_dict:
        horizontal_solar_irradiance = horizontal_solar_irradiance_dict[date_time]
        # It's not the safest solution to use first dict's keys to manage second dict, but they have identical keys
        correction_factor = correction_factor_dict[date_time]
        solar_irradiance = horizontal_solar_irradiance * correction_factor
        solar_irradiance_dict[date_time] = solar_irradiance

    return solar_irradiance_dict


# Function to return horizontal solar irradiance in [W/m^2]
# Only datetime from clouds_dict will be used
# @params:  installation - installation object from class Installation
#           clouds_dict - dict with datetime and clouds forecast from get_hourly_forecast function
def get_horizontal_solar_irradiance(installation, clouds_dict):
    # Plane pointing zenith
    v_norm = np.array([0, 0, -1])
    # Installation parameters
    altitude = installation.altitude
    latitude = installation.latitude
    # Solar Irradiance dict- as a key- datetime, as a value- solar irradiance
    solar_irradiance_dict = {}
    # For every element in clouds dict
    for date_time in clouds_dict:
        # Computed solar irradiance
        irradiance = irradiance_on_plane(v_norm, altitude, date_time, latitude)
        # Dict_name[key] = value
        solar_irradiance_dict[date_time] = irradiance

    return solar_irradiance_dict


# Function to get sun position for datetime, lat, long, timezone
# It returns sun elevation and sun azimuth in [deg], azimuth is a clockwise direction starting from north
# For example- North is 0 degrees azimuth
# @params:  installation - installation object from class Installation
#           clouds_dict - dict with datetime and clouds forecast from get_hourly_forecast function
def get_sun_position(installation, clouds_dict):
    # Installation parameters
    latitude = installation.latitude
    longitude = installation.longitude
    # Sun position dict- as a key- datetime, as a value- sun elevation and azimuth in a list
    sun_position_dict = {}
    # For every element in clouds dict
    for date_time in clouds_dict:
        # Timezone value in float type
        timezone = date_time.utcoffset().total_seconds() / 3600
        # Getting sun elevation and sun azimuth values from sunpos function
        sun_elevation, sun_azimuth = sunpos(date_time, latitude, longitude, timezone, dst=False)
        # Dict_name[key] = value
        sun_position_dict[date_time] = [sun_azimuth, sun_elevation]

    return sun_position_dict


# Function to get correction factor of irradiance on tilted pv installation
# @params:  installation - installation object from class Installation
#           sun_position_dict - dict with datetime and sun position from sun_position function
def get_correction_factor(installation, sun_position_dict):
    # Parameters to formula
    lat = installation.latitude
    azi = installation.azimuth
    ele = installation.elevation
    # Correction factor dict: datetime is a key and correction factor is a value
    correction_factor_dict = {}
    # For every element in sun position dict
    for date_time in sun_position_dict:
        # Get sun azimuth and elevation from sun_position_dict, [azimuth, elevation] in list
        sun_azi = sun_position_dict[date_time][0]
        sun_ele = sun_position_dict[date_time][1]
        correction_factor = correction_factor_formula(lat, azi, ele, sun_azi, sun_ele)
        correction_factor_dict[date_time] = correction_factor

    return correction_factor_dict


# Function to compute and return correction factor value
# @params:  lat- installation latitude
#           azi- installation azimuth
#           ele- installation elevation
#           sun_azi- sun azimuth
#           sun_ele- sun elevation
def correction_factor_formula(lat, azi, ele, sun_azi, sun_ele):
    nominator_1 = math.sin(math.radians(sun_ele)) * (math.sin(math.radians(lat)) * math.cos(math.radians(ele))
                - math.cos(math.radians(lat)) * math.sin(math.radians(ele)) * math.cos(math.radians(azi)))
    nominator_2 = math.cos(math.radians(sun_ele)) * (math.cos(math.radians(lat)) * math.cos(math.radians(ele))
                * math.cos(math.radians(sun_azi)) + math.sin(math.radians(lat)) * math.sin(math.radians(ele))
                * math.cos(math.radians(azi)) * math.cos(math.radians(sun_azi)) + math.sin(math.radians(ele))
                * math.sin(math.radians(azi)) * math.sin(math.radians(sun_azi)))
    denominator = math.sin(math.radians(sun_ele)) * math.sin(math.radians(lat)) + math.cos(math.radians(sun_ele))\
                * math.cos(math.radians(lat)) * math.cos(math.radians(sun_azi))
    # Correction factor
    correction_factor = abs((nominator_1 + nominator_2) / denominator)

    return correction_factor


# Function to calculate relative insolation
# @params:  clouds_dict - dict with datetime and clouds forecast from get_hourly_forecast function
def get_relative_insolation(clouds_dict):
    # Parameters to formula
    empirical_coefficient = 0.0043   # For Poland
    # Relative insolation dict
    relative_insolation_dict = {}
    # For every element in clouds dict
    for date_time in clouds_dict:
        clouds = clouds_dict[date_time]
        # Relative insolation formula, divided by 100 to not return the result as %, only a fraction
        relative_insolation = ((100 - clouds) * (1 + empirical_coefficient * clouds) / 100)
        relative_insolation_dict[date_time] = relative_insolation

    return relative_insolation_dict
