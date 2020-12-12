import plotly
import formatting
import computing
from typing import *
import plotly.graph_objects as go


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


def plot_datasets(dataset: List[Tuple[int, float]]) -> None:
    """Create a plotly graph of all the datasets
        Before running,

        Red List:
                1. run 'add_red_list_species' function on data
        Global Temperature:
                1. run 'average_temperature_data'  on data

        Afterwards,
         all datasets must be put through 'dict_to_list_of_tuples' before this function.
    """
    # Create lists of usable values
    xcoords = [dataset[x][0] for x in range(len(dataset))]
    ycoords = [dataset[x][1] for x in range(len(dataset))]

    # Create a blank figure
    fig = go.Figure()

    # Add the given data
    fig.add_trace(go.Scatter(x=xcoords, y=ycoords,
                             mode='lines+markers', name='data'))
    # Naming of axis and title - NOT ACCURATE NEED TO PASS IN NAME AND Y AXIS LABEL
    fig.update_layout(title='Raw Dataset',
                      xaxis_title='Years',
                      yaxis_title='Number of ______')

    # Display the figure in a web browser.
    fig.show()
