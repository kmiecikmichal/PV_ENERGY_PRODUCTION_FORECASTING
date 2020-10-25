import pandas as pd


class User:
    def __init__(self, _user_id, name, power, azimuth, altitude, longitude, latitude):
        self._user_id = _user_id  # Unique user id
        self.name = name  # User name
        self.power = power  # Installation power in Watts
        self.azimuth = azimuth  # Azimuth of installation in degrees (Azymut)
        self.altitude = altitude  # Altitude of installation in degrees (Elewacja)
        self.longitude = longitude  # Longitude of installation (Dl. Geograficzna)
        self.latitude = latitude  # Latitude of installation (Szer. Geograficzna)

    def get_values(self):
        return self._user_id, self.name, self.power, self.azimuth, self.altitude, self.longitude, self.latitude

    def add_to_database(self):
        # Open database
        database_df = pd.read_csv("user_database.csv", sep=",", header=0)

        # Check by user_id if user exists in database
        if self._user_id in database_df.ID.values:
            # Add values to existing user
            database_df.loc[database_df.ID == self._user_id,
                            ["Name", "Power[W]", "Azimuth[deg]", "Altitude[deg]", "Longitude", "Latitude"]] = \
                            [self.name, self.power, self.azimuth, self.altitude, self.longitude, self.latitude]
        else:
            # Add new user with values
            new_user = {"ID": self._user_id,
                        "Name": self.name,
                        "Power[W]": self.power,
                        "Azimuth[deg]": self.azimuth,
                        "Altitude[deg]": self.altitude,
                        "Longitude": self.longitude,
                        "Latitude": self.latitude}
            database_df = database_df.append(new_user, ignore_index=True)

        # Save this list to csv file named user_database
        database_df.to_csv("user_database.csv", sep=",", index=False)
        print(database_df) ############################################################################# TEMPORARY PRINT

    def delete_from_database(self):
        # Open database
        database_df = pd.read_csv("user_database.csv", sep=",", header=0)

        # Check by user_id if user exists in database
        if self._user_id in database_df.ID.values:
            # Delete row with specified user_id
            database_df.drop(database_df.loc[database_df['ID'] == self._user_id].index, inplace=True)
        else:
            print("ERROR: user does not exist in database") ################################# Zmienić na try except może

        # Save this list to csv file named user_database
        database_df.to_csv("user_database.csv", sep=",", index=False)
        print(database_df)  ############################################################################ TEMPORARY PRINT
