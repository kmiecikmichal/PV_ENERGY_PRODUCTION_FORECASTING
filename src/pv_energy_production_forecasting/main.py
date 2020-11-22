import installation
import weather_forecast
import solar_irradiance
import installation_losses


if __name__ == "__main__":
    # Welcome in app
    print("Welcome in PV Energy Production Forecast app!")

    #Michal = installation.Installation(installation.get_id(), "Michal", 20000, 235, 13, 50.0263, 19.9647, 250, 40, -0.4, 1)
    #Michal.add_to_database()
    #Michal.delete_from_database()

    # Active Installation class object
    active_installation = installation.get_last_user()
    print(active_installation.get_values())

    # Data from Open Weather API
    api_data = weather_forecast.get_api_data(active_installation)
    # Hourly weather forecast for next 48h
    clouds, temperature = weather_forecast.get_hourly_forecast(active_installation, api_data)

    # Get solar irradiance
    solar_irr = solar_irradiance.get_solar_irradiance(active_installation, clouds)
    #for element in solar_irr:
    #    print(" DATETIME: ", element)
    #    print(" IRRADIANCE: ", solar_irr[element], "W/m^2")
    #    print(" CLOUDS: ", clouds[element], "%" "\n")

    # Get pv cell temperature
    pv_cell_temp = installation_losses.get_pv_cell_temperature(active_installation, temperature, solar_irr)

    # Get temperature losses in %
    temperature_losses = installation_losses.get_temperature_losses(active_installation, pv_cell_temp)
    print(temperature_losses)
