import random

import plotly
from plotly.graph_objs import Figure

import formatting
import computing
from typing import *
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def run() -> None:
    # Formatted data
    red_list_data = formatting.xlsx_to_data("data//red_list_data.xlsx")
    carbon_data = formatting.xlsx_to_data("data//carbon_dioxide_concentrations.xlsx")
    temperature_data = formatting.csv_to_data("data//global_land_temperatures.csv")
    natural_disasters_data = formatting.csv_to_data("data//natural_disasters_data.csv")
    formatting.add_red_list_species(red_list_data)
    computing.average_temperature_data(temperature_data)

    red_list_data, temperature_data, carbon_data, natural_disasters_data = \
        computing.same_year_data(red_list_data, temperature_data, carbon_data, natural_disasters_data)

    red_list_data = formatting.dict_to_tuple_of_lists(red_list_data)
    temperature_data = formatting.dict_to_tuple_of_lists(temperature_data)

    years = red_list_data[0]
    dep_val = red_list_data[1]
    indep_val = temperature_data[1]
    a, b = computing.simple_linear_regression((indep_val, dep_val))
    future_value = computing.predict_future_value(a, b, indep_val, 0.1) # find all 0.1 changes
    residuals = computing.residuals((indep_val, dep_val), a, b)
    standard_dev = computing.residual_standard_deviation(residuals)
    sigma = computing.prediction_interval_sigma(standard_dev)

    new_point_x = [indep_val[-1] + 0.1]
    new_point_y = [future_value]
    xmax = (indep_val[-1] + 0.1) + 0.1 * (indep_val[-1] + 0.1 - indep_val[0]) # only change second 0.1
    xmin = indep_val[0] - 0.1 * (indep_val[-1] - indep_val[0])
    plot_datasets(years, dep_val, indep_val, a, b, xmax, xmin, new_point_x, new_point_y, sigma)

    carbon_data = formatting.dict_to_tuple_of_lists(carbon_data)
    natural_disasters_data = formatting.dict_to_tuple_of_lists(natural_disasters_data)

    #computing.multiple_regression(red_list_data, temperature_data, carbon_data, natural_disasters_data)
    #plot_points_and_regression(temperature_data[1], red_list_data[1] + [future_value], a, b, 10,[temperature_data[1][-1] + 0.1], [future_value], standard_dev)




def evaluate_line(a: float, b: float, error: float, x: float) -> float:
    """Evaluate the linear function y = a + bx for the given a, b, and x values
    with the given error term.

    More precisely, this function first calculates a random number e between
    -error and error, inclusive, and then returns a + bx + e. When error == 0,
    this function simply returns a + bx.

    You may ASSUME that:
        - error >= 0

    Hint: use the random.uniform function, which takes in two numbers and
    returns a random number between them, inclusive. For example,
    random.uniform(-10, 10) returns a random number between -10 and 10.
    random.uniform(0, 0) returns 0.

    Because of the randomness, we can't specify an exact doctest, but we can
    write a doctest based on the range of possible values:

    >>> result = evaluate_line(5.0, 1.0, 0.5, 10.0)  # y = 5.0 + 1.0 * 10.0, with error 0.5
    >>> -0.5 <= result - 15.0 <= 0.5
    True
    >>> evaluate_line(6.0, 1.5, 0.0, 3.0)  # y = 6.0 + 1.5 * 3.0, with error 0.0
    10.5
    """

    e = random.uniform(-error, error)
    return a + b * x + e


def run_with_gui() -> None:
    """ Runs with graphical interface
    """
    import interface


def plot_datasets(graph1_x_coords: list, y_coords: list, graph2_x_coords: list, a: float, b: float, x_max: float, x_min:float,
                  new_point_x: list, new_point_y: list, sigma: float) -> None:
    """Create a plotly graph of the all the datasets apart from red list
        This function takes in a dictionary with one to one pairings only.
        The dictionaries are created by using the functions in formatting.py
    """
    # Create a blank figure
    fig = make_subplots(rows=1, cols=2)

    # Add the given data
    make_graph1(fig, graph1_x_coords, y_coords, graph2_x_coords, new_point_y, sigma)
    make_graph2(fig, graph2_x_coords, y_coords, x_min, x_max, a, b, new_point_x, new_point_y, sigma)

    # Naming of axis and title
    fig.update_layout(title='Raw Dataset',
                      xaxis_title='Years',
                      yaxis_title='Number of ______')

    # Display the figure in a web browser.
    fig.show()


def make_graph1(fig: Figure, graph1_x_coords: list, y_coords: list, graph2_x_coords:list, new_point_y: list, sigma: float) -> None:
    fig.add_trace(go.Scatter(x=graph1_x_coords, y=y_coords,
                             mode='lines+markers', name='data'), row=1, col=1)

    fig.add_trace(go.Scatter(x=graph1_x_coords, y=graph2_x_coords,
                             mode='lines+markers', name='data'), row=1, col=1)

    fig.add_trace(go.Scatter(x=[2020], y=new_point_y, mode='markers', name='Prediction Interval',
                             error_y=dict(type='constant', value=sigma)), row=1, col=1)


def make_graph2(fig: Figure, graph2_x_coords: list, y_coords: list, x_min: float, x_max: float,
                a: float, b: float, new_point_x: list, new_point_y: list, sigma: float):
    fig.add_trace(go.Scatter(x=graph2_x_coords, y=y_coords, mode='markers', name='Data'), row=1, col=2)

    # Add the regression line
    fig.add_trace(go.Scatter(x=[x_min, x_max], y=[evaluate_line(a, b, 0, x_min),
                                                  evaluate_line(a, b, 0, x_max)],
                             mode='lines', name='Regression line'), row=1, col=2)

    fig.add_trace(go.Scatter(x=new_point_x, y=new_point_y, mode='markers', name='Prediction Interval',
                             error_y=dict(type='constant', value=sigma)), row=1, col=2)
