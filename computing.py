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


def same_year_data(data1: dict, data2: dict, data3: dict, data4: dict) -> Tuple[Dict[int, float], Dict[int, float], Dict[int, float], Dict[int, float]]:
    """ Create datasets so the have the same years.
    """
    data1_new, data2_new, data3_new, data4_new = {}, {}, {}, {}
    for key in data1:
        if key in data2 and key in data3 and key in data4:
            data1_new[key] = data1[key]
            data2_new[key] = data2[key]
            data3_new[key] = data2[key]
            data4_new[key] = data2[key]

    return (data1_new, data2_new, data3_new, data4_new)


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
