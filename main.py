import random

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

    red_list_data, temperature_data = computing.same_year_data(red_list_data, temperature_data)
    red_list_data = formatting.convert_dict(red_list_data)
    temperature_data = formatting.convert_dict(temperature_data)
    a, b = computing.simple_linear_regression((temperature_data[1], red_list_data[1]))
    future_value = computing.predict_future_value(a, b, temperature_data[1], 0.1)

    residuals = computing.residuals((temperature_data[1], red_list_data[1]), a, b)
    standard_dev = computing.residual_standard_deviation(residuals)
    print(computing.prediction_interval(future_value, standard_dev))

    plot_points_and_regression(temperature_data[1], red_list_data[1], a, b, 10)


def plot_points_and_regression(x_coords: list, y_coords: list,
                               a: float, b: float, x_max: float) -> None:
    """Plot the given x- and y-coordinates and linear regression model using plotly.

    The linear regression model is the line y = a + bx.
    Like plot_points, this function displays the results in a web browser.

    Note: this function calls your evaluate_line function, so make sure that you've
    tested your evaluate_line function carefully before try to call this one.

    We've provided this function for you, and you should not modify it!
    """
    # Create a blank figure
    fig = go.Figure()

    # Add the raw data
    fig.add_trace(go.Scatter(x=x_coords, y=y_coords, mode='markers', name='Data'))

    # Add the regression line
    fig.add_trace(go.Scatter(x=[9, x_max], y=[evaluate_line(a, b, 0, 9),
                                              evaluate_line(a, b, 0, x_max)],
                             mode='lines', name='Regression line'))

    # Display the figure in a web browser
    fig.show()


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
