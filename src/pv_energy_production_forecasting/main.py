import installation
import weather_forecast


if __name__ == "__main__":
    # Welcome in app
    print("Welcome in PV Energy Production Forecast app!")

    #Michal = installation.Installation(installation.get_id(), "Michal", 20000, 20, 40, 50.026343, 19.964795, 1)
    #Michal.add_to_database()
    #Michal.delete_from_database()

    # Active Installation class object
    active_installation = installation.get_last_user()
    print(active_installation.get_values())

    # Data from Open Weather API
    api_data = weather_forecast.get_api_data(active_installation)
    # Hourly weather forecast for next 48h
    clouds, temperature = weather_forecast.get_hourly_forecast(active_installation, api_data)
