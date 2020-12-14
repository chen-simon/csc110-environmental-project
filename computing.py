"""
Computing Module

This module contains the functions that are needed to plot the data. The data is plotted with plotly.

This file is Copyright (c) 2020 Patricia Ding, Makayla Duffus, Simon Chen.
"""
import math
from typing import Dict, List, Tuple
from sklearn.linear_model import LinearRegression
import pandas


def average_temperature_data(data: Dict[int, List]) -> None:
    """ Calculate average temperature during each year. This function mutates the input data.

    The dictionary changes from the form Dict[int, List[float]] to Dict[int, float]
    upon mutation.

    >>> dataset = {1: [1, 2, 3], 2: [4, 5, 6]}
    >>> average_temperature_data(dataset)
    >>> dataset == {1: 2, 2: 5}
    True
    """
    for key in data:
        data[key] = sum(data[key]) / len(data[key])


def simple_linear_regression(points: Tuple[List[float], List[float]]) -> Tuple[float, float]:
    """Perform a simple linear regression on the given points. This function returns a pair of floats (a, b) such
    that the line y = a + bx is the approximation of this data.

    >>> simple_linear_regression(([0, 1, 2, 3], [0, 1, 2, 3]))
    (0.0, 1.0)
    """

    x_values = points[0]
    y_values = points[1]
    x_avg = sum(x_values) / len(x_values)
    y_avg = sum(y_values) / len(y_values)

    b_top = sum([(x_values[z] - x_avg) * (y_values[z] - y_avg) for z in range(0, len(x_values))])
    b_bottom = sum([(x_values[z] - x_avg) ** 2 for z in range(0, len(x_values))])
    b = b_top / b_bottom

    a = y_avg - b * x_avg

    return (a, b)


def same_year(red_list_data: Dict[int, float], temperature_data: Dict[int, float],
              natural_disasters_data: Dict[int, float], carbon_data: Dict[int, float]) -> Tuple[Dict[int, float],
                                                                                                Dict[int, float],
                                                                                                Dict[int, float],
                                                                                                Dict[int, float]]:
    """ Return a tuple of dictionaries that all contain the same years as keys

    >>> same_year({2002: 2, 2000: 2}, {2004: 2, 2000: 3}, {2001: 2, 2000: 4}, {2007: 2, 2000: 5})
    ({2000: 2}, {2000: 3}, {2000: 4}, {2000: 5})
    """
    new_red_list, new_temp_data, new_disasters_data, new_carbon_data = {}, {}, {}, {}

    for year in red_list_data:
        if year in temperature_data and year in natural_disasters_data and year in carbon_data:
            new_red_list[year] = red_list_data[year]
            new_temp_data[year] = temperature_data[year]
            new_disasters_data[year] = natural_disasters_data[year]
            new_carbon_data[year] = carbon_data[year]

    return (new_red_list, new_temp_data, new_disasters_data, new_carbon_data)


def predict_future_value(a: float, b: float, data: List[float], change: float) -> float:
    """ Return the predicted value based on the simple linear regression.
    """
    return a + b * (data[-1] + change)


def calculate_r_squared(x_values: List[float], y_values: List[float], a: float, b: float) -> float:
    """Return the R squared value when the given points are modelled as the line y = a + bx.
    """
    y_average = sum(y_values) / len(y_values)

    s_tot = sum([(y_values[x] - y_average) ** 2 for x in range(0, len(y_values))])
    s_res = sum([(y_values[x] - (a + b * x_values[x])) ** 2 for x in range(0, len(y_values))])

    return 1 - s_res / s_tot


def residuals(data: Tuple[List[float], List[float]], a: float, b: float) -> List[float]:
    """ Return the residual values of the linear regression.
    """
    nums_so_far = []
    for i in range(0, len(data[1])):
        residual = data[1][i] - (a + b * data[0][i])
        nums_so_far.append(residual)

    return nums_so_far


def residual_standard_deviation(residual_list: List[float]):
    """ Return the standard deviation of the residual values.
    """
    squared_residuals = [residual ** 2 for residual in residual_list]
    standard_dev = math.sqrt(sum(squared_residuals) / (len(squared_residuals) - 2))
    return standard_dev


def prediction_interval_sigma(standard_dev: float) -> float:
    """ Return the +- value of an 80% prediction interval.
    """
    return standard_dev * 1.28


def multiple_regression2(red_list_data: Tuple[List[float], List[float]], dataset1: Tuple[List[float], List[float]],
                         dataset2: Tuple[List[float], List[float]], value1: float, value2: float) -> float:
    """ Return the prediction of a multiple linear regression with two variables.
    """
    y = pandas.DataFrame(red_list_data[1])
    x = pandas.DataFrame(list(zip(dataset1[1], dataset2[1])))
    linear_regression = LinearRegression()
    linear_regression.fit(x, y)
    y_pred = linear_regression.predict([[value1, value2]])
    return float(y_pred)


def multiple_regression3(red_list_data: Tuple[List[float], List[float]], dataset1: Tuple[List[float], List[float]],
                         dataset2: [List[float], List[float]], dataset3: tuple, value1: float, value2: float,
                         value3: float) -> float:
    """ Return the prediction of a multiple linear regression with three variables.
    """
    y = pandas.DataFrame(red_list_data[1])
    x = pandas.DataFrame(list(zip(dataset1[1], dataset2[1], dataset3[1])))
    linear_regression = LinearRegression()
    linear_regression.fit(x, y)
    y_pred = linear_regression.predict([[value1, value2, value3]])
    return float(y_pred)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
