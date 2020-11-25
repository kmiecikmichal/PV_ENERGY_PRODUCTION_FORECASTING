import json
import requests
import pytz
from timezonefinder import TimezoneFinder
from datetime import datetime


# Function to read Open Weather API key from file api_key.txt
def get_api_key():
    # Open api_key.txt file containing key for Open Weather API
    with open("api_key.txt") as f:
        api_key = f.read()

    return api_key


# Function to get data from Open Weather API
# @params:  installation - installation object from class Installation
def get_api_data(installation):
    # Set variables needed to get requested data from Open Weather API
    api_key = get_api_key()
    latitude = installation.latitude
    longitude = installation.longitude
    address = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric"

    # Url address to send request to
    url = address % (latitude, longitude, api_key)
    # Getting reply for our request
    reply = requests.get(url)
    # Data received from API
    api_data = json.loads(reply.text)

    return api_data


# Function to get hourly forecasts from API data
# @params:  installation - installation object from class Installation
#           api_data - API Result data (return from function get_api_data)
def get_hourly_forecast(installation, api_data):
    # Get hourly forecast from api_data
    hourly_forecast = api_data["hourly"]
    # Get timezone object
    timezone = get_timezone(installation)

    # Dicts, where datetime will be a key, and forecasts will be values
    clouds = {}
    temperature = {}
    for entry in hourly_forecast:
        # Get datetime from timestamp
        date_time = datetime.fromtimestamp(entry["dt"], timezone)
        # Dict_name[key] = value
        clouds[date_time] = entry["clouds"]
        temperature[date_time] = entry["temp"]

    return clouds, temperature


# Function to get timezone object from pytz and timezone finder library
# @params:  installation - installation object from class Installation
def get_timezone(installation):
    # Get latitude and longitude from object
    latitude = installation.latitude
    longitude = installation.longitude
    # Get timezone id
    tf = TimezoneFinder()
    timezone_id = tf.timezone_at(lat=latitude, lng=longitude)
    # Get timezone object
    timezone = pytz.timezone(timezone_id)

    return timezone
