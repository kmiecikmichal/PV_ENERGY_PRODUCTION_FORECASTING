import pandas as pd
import sys


class Installation:
    def __init__(self, _id, name, power, azimuth, elevation, latitude, longitude, altitude, pv_cell_temp_noct, _used):
        self._id = _id  # Unique installation id
        self.name = name  # Installation name
        self.power = power  # Installation power in Watts
        self.azimuth = azimuth  # Azimuth of installation in degrees, deviation from south (S = 0[deg]) (Azymut)
        self.elevation = elevation  # Elevation angle of installation in degrees (Elewacja)
        self.latitude = latitude  # Latitude of installation (Szer. Geograficzna)
        self.longitude = longitude  # Longitude of installation (Dl. Geograficzna)
        self.altitude = altitude  # Altitude- Height above sea level
        self.pv_cell_temp_noct = pv_cell_temp_noct # Temperature of pv cell NOCT in Celsius degrees.
        self._used = _used  # Flag that indicates whether the object is currently in use

    def get_values(self):
        return self._id, self.name, self.power, self.azimuth, self.elevation, \
               self.latitude, self.longitude, self.altitude, self.pv_cell_temp_noct, self._used

    def add_to_database(self):
        # Open database
        try:
            database_df = pd.read_csv("installation_database.csv", sep=",", header=0)
        except FileNotFoundError:
            print("ERROR: File installation_database.csv not found")
            sys.exit(1)

        # Check by _id if installation exists in database
        if self._id in database_df.ID.values:
            # Add values to existing installation
            database_df.loc[database_df["ID"] == self._id,
            ["Name", "Power[W]", "Azimuth[deg]", "Elevation[deg]", "Latitude", "Longitude", "Altitude", "Used"]] = \
            [self.name, self.power, self.azimuth, self.elevation, self.latitude, self.longitude, self.altitude,
             self.pv_cell_temp_noct, self._used]
        else:
            # Add new installation with values
            new_installation = {"ID": self._id,
                                "Name": self.name,
                                "Power[W]": self.power,
                                "Azimuth[deg]": self.azimuth,
                                "Elevation[deg]": self.elevation,
                                "Latitude": self.latitude,
                                "Longitude": self.longitude,
                                "Altitude": self.altitude,
                                "PVCellTempNOCT[deg.C]": self.pv_cell_temp_noct,
                                "Used": self._used}
            database_df = database_df.append(new_installation, ignore_index=True)

        # Save this list to csv file named installation_database
        database_df.to_csv("installation_database.csv", sep=",", index=False)
        print(database_df)  ########################################################################## TEMPORARY PRINT

    def delete_from_database(self):
        # Open database
        database_df = pd.read_csv("installation_database.csv", sep=",", header=0)

        # Check by _id if installation exists in database
        if self._id in database_df.ID.values:
            # Delete row with specified _id
            database_df.drop(database_df.loc[database_df['ID'] == self._id].index, inplace=True)
            # Change state of ID of deleted object from used ("1") to unused ("0")
            drop_id(self._id)
        else:
            print("ERROR: installation does not exist in database")  ###################### Zmienić na try except może

        # Save this list to csv file named installation_database
        database_df.to_csv("installation_database.csv", sep=",", index=False)
        print(database_df)  ######################################################################### TEMPORARY PRINT


# Function to get unused ID from id_database and set it as an attribute of Installation class object
# Use only when user generates new installation
def get_id():
    # Open id_database
    try:
        database_df = pd.read_csv("id_database.csv", sep=",", header=0)
    except FileNotFoundError:
        print("ERROR: File id_database.csv not found")
        sys.exit(1)

    # Get first row with "Used" value set as "0"
    id_row = database_df[database_df["Used"] == 0].iloc[0]
    # Set "Used" value as "1"
    database_df.loc[database_df["ID"] == id_row["ID"], ["Used"]] = 1
    # Save id_database file
    database_df.to_csv("id_database.csv", sep=",", index=False)
    # Return id value
    return id_row["ID"]


# Function to change state of ID of deleted object from used ("1") to unused ("0")
# @params:  user_id - ID of deleted user
def drop_id(user_id):
    # Open id_database
    try:
        database_df = pd.read_csv("id_database.csv", sep=",", header=0)
    except FileNotFoundError:
        print("ERROR: File id_database.csv not found")
        sys.exit(1)

    # Get row with specified ID
    database_df.loc[database_df["ID"] == user_id, ["Used"]] = 0
    # Save id_database file
    database_df.to_csv("id_database.csv", sep=",", index=False)


# Function to get from installation_database last used installation
# Used when the program starts
# Returns active installation object of class Installation
def get_last_user():
    # Open installation_database.csv
    try:
        database_df = pd.read_csv("installation_database.csv", sep=",", header=0)
    except FileNotFoundError:
        print("ERROR: File installation_database.csv not found")
        sys.exit(1)

    # Get first (and only) row with "Used" value set as "1"
    used_row = database_df[database_df["Used"] == 1].iloc[0]
    # Make Installation class object with attributes from database
    active_installation = Installation(used_row["ID"],
                                       used_row["Name"],
                                       float(used_row["Power[W]"]),
                                       float(used_row["Azimuth[deg]"]),
                                       float(used_row["Elevation[deg]"]),
                                       float(used_row["Latitude"]),
                                       float(used_row["Longitude"]),
                                       float(used_row["Altitude"]),
                                       float(used_row["PVCellTempNOCT[deg.C]"]),
                                       int(used_row["Used"]))
    # Return installation object
    return active_installation


"""
def read_installation_database():
    # Open database
    try:
        database_df = pd.read_csv("installation_database.csv", sep=",", header=0) 
    except FileNotFoundError:
        print("ERROR: File installation_database.csv not found")
        sys.exit(1)

    # Make a dict from ID and Name and return it
    database_dict = database_df.set_index("ID")["Name"].to_dict()
    return database_df, database_dict


def manage_installation_database():
    # Take dict with {ID: Name} from database
    database_df, database_dict = read_installation_database()

    # Ask user if he wants to use existing installation or make new one
    print("If you want to add new account, press 0")
    print("If you want to use existing account, press 1")
    print("If you want to delete existing account, press 2")
    input_val_1 = input("Enter your value: ")

    # If user wants to add new installation:
    if input_val_1 == "0":
        print("New account creator")
        # Enter needed values to make a installation object from class Installation
        input_val_2_1_1 = input("Installation ID [Uxx]: ")
        input_val_2_1_2 = input("Installation Name: ")
        input_val_2_1_3 = input("Power in Watts: ")
        input_val_2_1_4 = input("Azimuth in degrees: ")
        input_val_2_1_5 = input("Elevation in degrees: ")
        input_val_2_1_6 = input("Latitude: ")
        input_val_2_1_7 = input("Longitude: ")
        # ADD ALTITUDE -------------------------------------
        # ADD TEMP NOCT ------------------------------------
        # ADD USED------------------------------------------------

        installation = Installation(input_val_2_1_1,
                    input_val_2_1_2,
                    input_val_2_1_3,
                    input_val_2_1_4,
                    input_val_2_1_5,
                    input_val_2_1_6,
                    input_val_2_1_7)
                    # ADD ALTITUDE  ----------------------------
                    # ADD TEMP NOCT ------------------------------------
                    # ADD USED ---------------------------------------

        # Add new installation to database
        installation.add_to_database()


    # If user wants to use existing installation
    elif input_val_1 == "1":
        # If database is empty, warn about it
        if not bool(database_dict):
            print("ERROR: Database is empty")
        else:
            # Ask user which one he wants to choose
            print("Press number with installation you want to choose. If you want to cancel, press 'c'")
            # Print dict with available installations
            for i in enumerate(database_dict.items()):
                print(i)
            input_val_2_2 = input("Enter your value: ")
            # If not cancel, make an object from class Installation
            if input_val_2_2 != "c":
                installation = Installation(database_df["ID"][int(input_val_2_2)],
                            database_df["Name"][int(input_val_2_2)],
                            float(database_df["Power[W]"][int(input_val_2_2)]),
                            float(database_df["Azimuth[deg]"][int(input_val_2_2)]),
                            float(database_df["Elevation[deg]"][int(input_val_2_2)]),
                            float(database_df["Latitude"][int(input_val_2_2)]),
                            float(database_df["Longitude"][int(input_val_2_2)]))
                            # ADD ALTITUDE -----------------------------------
                            # ADD TEMP NOCT ------------------------------------
                            # ADD USED ----------------------------------------------

    # If user wants to delete existing installation
    elif input_val_1 == "2":
        # If database is empty, warn about it
        if not bool(database_dict):
            print("ERROR: Database is empty")
        else:
            # Ask user which one he wants to delete
            print("Press number with installation you want to delete. If you want to cancel, press 'c'")
            # Print dict with available installations
            for i in enumerate(database_dict.items()):
                print(i)
            input_val_2_3 = input("Enter your value: ")
            # If not cancel, make an object from class Installation
            if input_val_2_3 != "c":
                installation = Installation(database_df["ID"][int(input_val_2_3)],
                            database_df["Name"][int(input_val_2_3)],
                            float(database_df["Power[W]"][int(input_val_2_3)]),
                            float(database_df["Azimuth[deg]"][int(input_val_2_3)]),
                            float(database_df["Elevation[deg]"][int(input_val_2_3)]),
                            float(database_df["Latitude"][int(input_val_2_3)]),
                            float(database_df["Longitude"][int(input_val_2_3)]))
                            # ADD ALTITUDE --------------------------------------
                            # ADD TEMP NOCT ------------------------------------
                            # ADD USED -------------------------------------------------
                # And delete this object from database
                installation.delete_from_database()

    else:
        print("ERROR: Unrecognized value input_val_1")
"""
