import installation
import pandas as pd


if __name__ == "__main__":
    # Welcome in app
    print("Welcome in PV Energy Production Forecast app!")

    # Michal = installation.Installation(installation.get_id(), "Michal", 20000, 20, 40, 40.002, 21.008, 1)
    #Michal.add_to_database()
    #Michal.delete_from_database()

    # Active Installation class object
    active_installation = installation.get_last_user()
    print(active_installation.get_values())
