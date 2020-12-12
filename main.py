import plotly
import formatting
import computing
from typing import *


def run() -> None:
    # Formatted data
    red_list_data = formatting.xlsx_to_data("data//red_list_data.xlsx")
    carbon_data = formatting.xlsx_to_data("data//carbon_dioxide_concentrations.xlsx")
    temperature_data = formatting.csv_to_data("data//global_land_temperatures.csv")
    natural_disasters_data = formatting.csv_to_data("data//natural_disasters_data.csv")

    formatting.add_red_list_species(red_list_data)
    computing.average_temperature_data(temperature_data)

    print(red_list_data)
    print(carbon_data)
    print(temperature_data)
    print(natural_disasters_data)


def run_with_gui() -> None:
    """ Runs with graphical interface
    """
    import interface
