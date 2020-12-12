import math
from typing import Tuple, List, Dict


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


def same_year_data(data1: dict, data2: dict) -> Tuple[Dict[int, float], Dict[int, float]]:
    """ Create datasets so the have the same years.
    """
    data1_new ={}
    data2_new ={}
    for key in data1:
        if key in data2:
            data1_new[key] = data1[key]
            data2_new[key] = data2[key]

    return (data1_new, data2_new)


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


def prediction_interval(predicted_value: float, standard_dev: float) -> Tuple[float, float]:
    """ 80% prediction interval
    """
    lower_num = predicted_value - standard_dev * 1.28
    upper_num = predicted_value + standard_dev * 1.28
    return (lower_num, upper_num)
