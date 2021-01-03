import installation
import data_visualisation
import production_calculation
import weather_forecast

import tkinter.ttk as ttk

import tkinter as tk
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "Pv Forecasting App")
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        # Get active installation object
        active_installation = installation.get_last_user()

        tk.Label(self, text="Active installation:\n" + active_installation.name,
                 font=font_header).pack(side="top", fill="x", pady=20)
        tk.Button(self, text="Forecast", font=font_button,
                  command=lambda: master.switch_frame(PageOne)).pack(pady=5)
        tk.Button(self, text="Switch installation", font=font_button,
                  command=lambda: master.switch_frame(PageTwo)).pack(pady=5)


class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg="white")

        tk.Button(self, text="Back", font=font_button,
                  command=lambda: master.switch_frame(StartPage)).pack(side="bottom", pady=10)

        # VISUALISE DATA
        # Get active installation object
        active_installation = installation.get_last_user()
        # Get production calculation dict (keys: datetime objects, values: momentary power forecasts
        power_prod_forecast, energy_prod_forecast = production_calculation.production_calculation(active_installation)
        # Get timezone for matplotlib settings
        timezone = weather_forecast.get_timezone(active_installation)
        # Get the figure from data_visualisation file
        figure = data_visualisation.visualisation(timezone, power_prod_forecast, energy_prod_forecast)
        # Make canvas with matplotlib figure
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        # Add matplotlib toolbar to figure
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.tkcanvas.pack()


class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg='white')
        tk.Label(self, text="Switch installation", font=font_header, bg="white").pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Back", font=font_button,
                  command=lambda: master.switch_frame(StartPage)).pack(pady=5)

        # Table
        # Get dict with installation ids and names
        installation_database_dict = installation.get_installation_database()
        # Transform installation database dict to lists
        installation_id_list = []
        installation_name_list = []
        for installation_id in installation_database_dict:
            installation_name = installation_database_dict[installation_id]
            installation_name_list.append(installation_name)
            installation_id_list.append(installation_id)

        list_label = tk.Listbox(self)

        for item in installation_name_list:
            list_label.insert('end', item)
        list_label.pack()


if __name__ == "__main__":
    # Fonts
    font_header = ("Verdana", 16)
    font_button = ("Verdana", 12)
    # Make app instance
    app = Application()
    # App in loop
    app.mainloop()
