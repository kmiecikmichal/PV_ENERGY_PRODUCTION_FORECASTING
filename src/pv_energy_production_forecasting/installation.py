import pandas as pd
import sys


class Installation:
    def __init__(self, _id, name, power, azimuth, altitude, longitude, latitude, _used):
        self._id = _id  # Unique installation id
        self.name = name  # Installation name
        self.power = power  # Installation power in Watts
        self.azimuth = azimuth  # Azimuth of installation in degrees (Azymut)
        self.altitude = altitude  # Altitude of installation in degrees (Elewacja)
        self.longitude = longitude  # Longitude of installation (Dl. Geograficzna)
        self.latitude = latitude  # Latitude of installation (Szer. Geograficzna)
        self._used = _used  # Flag that indicates whether the object is currently in use

    def get_values(self):
        return self._id, self.name, self.power, self.azimuth, self.altitude, self.longitude, self.latitude, self._used

    def add_to_database(self):
        # Open database
        database_df = pd.read_csv("installation_database.csv", sep=",", header=0)

        # Check by _id if installation exists in database
        if self._id in database_df.ID.values:
            # Add values to existing installation
            database_df.loc[database_df["ID"] == self._id,
            ["Name", "Power[W]", "Azimuth[deg]", "Altitude[deg]", "Longitude", "Latitude", "Used"]] = \
            [self.name, self.power, self.azimuth, self.altitude, self.longitude, self.latitude, self._used]
        else:
            # Add new installation with values
            new_installation = {"ID": self._id,
                                "Name": self.name,
                                "Power[W]": self.power,
                                "Azimuth[deg]": self.azimuth,
                                "Altitude[deg]": self.altitude,
                                "Longitude": self.longitude,
                                "Latitude": self.latitude,
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
# @param: id - ID of deleted user
def drop_id(id):
    # Open id_database
    try:
        database_df = pd.read_csv("id_database.csv", sep=",", header=0)
    except FileNotFoundError:
        print("ERROR: File id_database.csv not found")
        sys.exit(1)

    # Get row with specified ID
    database_df.loc[database_df["ID"] == id, ["Used"]] = 0
    # Save id_database file
    database_df.to_csv("id_database.csv", sep=",", index=False)


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
        input_val_2_1_5 = input("Altitude in degrees: ")
        input_val_2_1_6 = input("Logtitude: ")
        input_val_2_1_7 = input("Latitude: ")

        installation = Installation(input_val_2_1_1,
                    input_val_2_1_2,
                    input_val_2_1_3,
                    input_val_2_1_4,
                    input_val_2_1_5,
                    input_val_2_1_6,
                    input_val_2_1_7)

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
                            float(database_df["Altitude[deg]"][int(input_val_2_2)]),
                            float(database_df["Longitude"][int(input_val_2_2)]),
                            float(database_df["Latitude"][int(input_val_2_2)]))


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
                            float(database_df["Altitude[deg]"][int(input_val_2_3)]),
                            float(database_df["Longitude"][int(input_val_2_3)]),
                            float(database_df["Latitude"][int(input_val_2_3)]))
                # And delete this object from database
                installation.delete_from_database()

    else:
        print("ERROR: Unrecognized value input_val_1")
"""
