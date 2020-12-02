import matplotlib.pyplot as plt


# Function to visualise momentary power forecasts
# @params:  production_calculation_dict - dictionary with forecasted production
def momentary_power_visualisation(production_calculation_dict):
    # Make lists for visualisation data storage
    datetime_list = []
    production_forecast_list = []
    for element in production_calculation_dict:
        # Change datetype type to string to make it readable for matplotlib
        datetime_string = element.strftime("%d.%m %H:%M")
        datetime_list.append(datetime_string)
        # Extract production forecast data from dict and put it into list
        production_forecast = production_calculation_dict[element]
        production_forecast_list.append(production_forecast)

    # Make plot
    plt.plot(datetime_list, production_forecast_list)
    # y axis label
    plt.ylabel("Moc chwilowa [W]")
    # Rotate date ticks (x axis)
    plt.xticks(datetime_list, rotation=45)
    # Choose amount of x ticks to be displayed
    plt.locator_params(axis='x', nbins=24)
    # Grid
    plt.grid(True)
    # Title
    plt.title('Wykres Mocy chwilowej instalacji pv od czasu')
    # Show the plot
    plt.show()
