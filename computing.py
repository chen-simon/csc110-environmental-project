import math
from typing import Tuple, List, Dict
from sklearn.linear_model import LinearRegression
import numpy
import pandas


def average_temperature_data(data: dict) -> None:
    """ Calculate average temperature during each year. This function mutates the input data.

    The dictionary changes from the form Dict[int, List[float]] to Dict[int, float]
    upon mutation.
    """
    for key in data:
        data[key] = sum(data[key]) / len(data[key])


def simple_linear_regression(points: tuple) -> tuple:
    """Perform a linear regression on the given points.

    points is a list of pairs of floats: [(x_1, y_1), (x_2, y_2), ...]
    This function returns a pair of floats (a, b) such that the line
    y = a + bx is the approximation of this data.

    You may ASSUME that:
        - len(points) > 0
        - each element of points is a tuple of two floats
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


def same_year(data:tuple, temperature: bool):
    data_so_far = ([], [])
    for i in range(0, len(data[0])):
        if data[0][i] > 1995 and data[0][i] != 1997 and data[0][i] != 1999 and data[0][i] != 2001 and data[0][i] != 2005:
            data_so_far[0].append(data[0][i])
            data_so_far[1].append(data[1][i])

    if temperature:
        for i in range(0, 4):
            data[0].pop()
            data[1].pop()
    return data_so_far


def predict_future_value(a: int, b: int, data: list, change: float) -> float:
    return a + b *(data[-1] + change)


def residuals(data: tuple, a: float, b: float) -> List[int]:
    """ Calculate residual values.
    """
    nums_so_far = []
    for i in range(0, len(data[1])):
        residual = data[1][i] - (a + b * data[0][i])
        nums_so_far.append(residual)

    return nums_so_far


def residual_standard_deviation(residual_list: list):
    squared_residuals = [residual ** 2 for residual in residual_list]
    standard_dev = math.sqrt(sum(squared_residuals) / (len(squared_residuals) - 2))
    return standard_dev


def prediction_interval_sigma(standard_dev: float) -> float:
    """ 80% prediction interval
    """
    return standard_dev * 1.28


def multiple_regression(red_list_data: tuple, temp: tuple, carbon: tuple, natural: tuple):
    y = pandas.DataFrame(red_list_data[1])
    x = pandas.DataFrame(list(zip(temp[1], carbon[1], natural[1])))
    print(x)
    linear_regression = LinearRegression()
    linear_regression.fit(x, y)
    y_pred = linear_regression.predict([[9.9, 330, 380]])
    print(y_pred)
