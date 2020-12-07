import weather_forecast
import solar_irradiance
import installation_losses


# Function to return production of momentary power forecasts, calculated from data from installation_database, and
# in form of dict, keys: datetime objects, values: momentary power forecasts
# @params:  active_installation - active installation object from class installation
def production_calculation(active_installation):

    # Data from Open Weather API
    api_data = weather_forecast.get_api_data(active_installation)

    # Hourly weather forecast for next 48h
    clouds, temperature = weather_forecast.get_hourly_forecast(active_installation, api_data)

    # Get solar irradiance
    solar_irr = solar_irradiance.get_solar_irradiance(active_installation, clouds)

    # Get temp and irradiance losses
    inst_efficiency = installation_losses.get_installation_efficiency(active_installation, temperature, solar_irr)

    # Momentary power forecast dict
    power_production_forecast_dict = {}
    # Energy production forecast dict
    energy_production_forecast_dict = {}
    # Initialize energy production forecast variable (used in loop)
    energy_production_forecast = 0

    for element in inst_efficiency:
        # Calculate power production forecast
        power_production_forecast = active_installation.installation_power * inst_efficiency[element]
        # Calculate energy production forecasts (reset value when no production)
        if power_production_forecast != 0:
            # Adding power production because it's hourly forecast (kW -> kWh)
            energy_production_forecast += power_production_forecast
        else:
            energy_production_forecast = 0
        # Pack these values into dicts
        power_production_forecast_dict[element] = power_production_forecast
        energy_production_forecast_dict[element] = energy_production_forecast

    return power_production_forecast_dict, energy_production_forecast_dict
