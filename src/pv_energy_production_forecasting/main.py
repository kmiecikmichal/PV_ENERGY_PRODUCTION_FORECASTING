import installation
import data_visualisation
import production_calculation


if __name__ == "__main__":
    # Welcome in app
    print("Welcome in PV Energy Production Forecast app!")

    #Michal = installation.Installation(installation.get_id(), "Michal", 20, 55, 15, 50.0263, 19.9647, 250, 40, 0.05, -0.33, 4.53, 9.15, 0.636, 1)
    #Michal.add_to_database()
    #Michal.delete_from_database()

    # Active Installation class object
    active_installation = installation.get_last_user()
    print(active_installation.get_values())

    # Get production calculation dict (keys: datetime objects, values: momentary power forecasts
    production_forecast = production_calculation.production_calculation(active_installation)


