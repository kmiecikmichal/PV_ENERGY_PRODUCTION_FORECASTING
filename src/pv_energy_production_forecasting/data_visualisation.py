import matplotlib
from matplotlib import dates
import matplotlib.pyplot as plt
from scipy.interpolate import pchip
import numpy as np


# Function to visualise momentary power forecasts
# @params:  production_calculation_dict - dictionary with forecasted production
def momentary_power_visualisation(timezone, power_production_forecast_dict, energy_production_forecast_dict):
    # Set proper matplotlib timezone
    matplotlib.rcParams['timezone'] = timezone

    # Make lists for visualisation data storage
    datetime_list = []
    power_production_forecast_list = []
    energy_production_forecast_list = []
    for element in power_production_forecast_dict:
        # Add datetime objects to list
        datetime_list.append(element)
        # Extract production forecasts data from dicts and put it into lists
        power_production_forecast = power_production_forecast_dict[element]
        energy_production_forecast = energy_production_forecast_dict[element]
        power_production_forecast_list.append(power_production_forecast)
        energy_production_forecast_list.append(energy_production_forecast)

    # Translate datetime objects to floats to interpolate data
    datetime_float = np.array([dates.date2num(i) for i in datetime_list])
    # Interpolation function of power production (numpy array is pchip function requirement)
    power_interpolation_function = pchip(datetime_float, np.array(power_production_forecast_list))
    # Interpolation function of energy production
    energy_interpolation_function = pchip(datetime_float, np.array(energy_production_forecast_list))
    # Interpolated datetime
    datetime_interpolated = np.linspace(datetime_float.min(), datetime_float.max(), num=192)
    # Interpolated power production
    power_production_interpolated = power_interpolation_function(datetime_interpolated)
    # Interpolated energy production
    energy_production_interpolated = energy_interpolation_function(datetime_interpolated)

    # Create figure
    figure = plt.figure()
    # Add subplot
    ax1 = figure.add_subplot(111)

    # Power production plot color
    power_plot_color = "tab:blue"
    # Power production y axis label
    ax1.set_ylabel("Instantaneous power [kW]", color=power_plot_color)
    ax1.tick_params(axis='y', labelcolor=power_plot_color)
    # Power production plot with interpolation
    ax1.plot(datetime_interpolated, power_production_interpolated, color=power_plot_color)

    # Rotate date ticks (x axis)
    plt.xticks(rotation=45)
    # Concise Date Formatter xticks
    locator = matplotlib.dates.AutoDateLocator(minticks=16, maxticks=24)
    formatter = matplotlib.dates.ConciseDateFormatter(locator)
    ax1.xaxis.set_major_locator(locator)
    ax1.xaxis.set_major_formatter(formatter)

    # New axes (for double y axes)
    ax2 = ax1.twinx()

    # Energy production plot color
    energy_plot_color = "tab:red"
    # Energy production y axis label
    ax2.set_ylabel("Energy production [kWh]", color=energy_plot_color)
    ax2.tick_params(axis='y', labelcolor=energy_plot_color)
    # Energy production plot with interpolation
    ax2.plot(datetime_interpolated, energy_production_interpolated, color=energy_plot_color)


    # Title
    ax1.set_title('Power and energy production vs time')
    # Grid
    ax1.grid()
    # Tight layout
    plt.tight_layout()

    return figure
