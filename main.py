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


def plot_red_list(dataset: Dict[str, List[int]]) -> None:
    """Create a plotly graph of the red list dataset

        This function only works for the red list dataset.
    """
    # Create lists of usable values
    xcoords = [int(x) for x in dataset.keys()]
    ycoords = [tuple(x) for x in dataset.values()]

    # Create a blank figure
    fig = go.Figure()

    # Add the given data
    fig.add_trace(go.Scatter(x=xcoords, y=[ycoords[x][0] for x in range(len(ycoords))],
                             mode='lines+markers', name='Vertebrates'))
    fig.add_trace(go.Scatter(x=xcoords, y=[ycoords[x][1] for x in range(len(ycoords))],
                             mode='lines+markers', name='Invertebrates'))
    fig.add_trace(go.Scatter(x=xcoords, y=[ycoords[x][2] for x in range(len(ycoords))],
                             mode='lines+markers', name='Plants'))
    fig.add_trace(go.Scatter(x=[x for x in xcoords if x > 2002], y=[ycoords[x][3] for x in range(len(ycoords))],
                             mode='lines+markers', name='Fungi &Protists'))
    fig.update_layout(title='Species on the Red List up to 2019',
                      xaxis_title='Years',
                      yaxis_title='Number of Animals')

    # Display the figure in a web browser.
    fig.show()


def plot_datasets(dataset: dict) -> None:
    """Create a plotly graph of the all the datasets apart from red list

        This function takes in a dictionary with one to one pairings only.
        The dictionaries are created by using the functions in formatting.py
    """
    # Create lists of usable values
    xcoords = [x for x in dataset.keys()]
    ycoords = [x for x in dataset.values()]

    # Create a blank figure
    fig = go.Figure()

    # Add the given data
    fig.add_trace(go.Scatter(x=xcoords, y=ycoords,
                             mode='lines+markers', name='data'))
    # Naming of axis and title
    fig.update_layout(title='Raw Dataset',
                      xaxis_title='Years',
                      yaxis_title='Number of ______')

    # Display the figure in a web browser.
    fig.show()
