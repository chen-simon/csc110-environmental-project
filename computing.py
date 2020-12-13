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


def same_year(red_list_data: dict, temperature_data: dict, natural_disasters_data: dict, carbon_data: dict):
    """ Return a dataset the matches the years of the red list data -- bad implementation will fix later
    """
    # data_so_far = ([], [])
    # for i in range(0, len(data[0])):
    #     if data[0][i] > 1995 and data[0][i] != 1997 and data[0][i] != 1999 and data[0][i] != 2001 and data[0][i] != 2005:
    #         data_so_far[0].append(data[0][i])
    #         data_so_far[1].append(data[1][i])
    #
    # if temperature:
    #     for i in range(0, 4):
    #         data[0].pop()
    #         data[1].pop()
    # return data_so_far
    new_red_list, new_temp_data, new_disasters_data, new_carbon_data = {}, {}, {}, {}

    for year in red_list_data:
        if year in temperature_data and year in natural_disasters_data and year in carbon_data:
            new_red_list[year] = red_list_data[year]
            new_temp_data[year] = temperature_data[year]
            new_disasters_data[year] = natural_disasters_data[year]
            new_carbon_data[year] = carbon_data[year]

    return new_red_list, new_temp_data, new_disasters_data, new_carbon_data


def predict_future_value(a: int, b: int, data: list, change: float) -> float:
    """ Return the predicted value based on the simple linear regression
    """
    return a + b *(data[-1] + change)


def calculate_r_squared(x_values: list, y_values: list, a: float, b: float) -> float:
    """Return the R squared value when the given points are modelled as the line y = a + bx.

    points is a list of pairs of numbers: [(x_1, y_1), (x_2, y_2), ...]

    Assume that:
        - points is not empty and contains tuples
        - each element of points is a tuple containing two floats
    """
    y_average = sum(y_values) / len(y_values)

    s_tot = sum([(y_values[x] - y_average) ** 2 for x in range(0, len(y_values))])
    s_res = sum([(y_values[x] - (a + b * x_values[x])) ** 2 for x in range(0, len(y_values))])

    return 1 - s_res / s_tot


def residuals(data: tuple, a: float, b: float) -> List[int]:
    """ Return the residual values of the linear regression.
    """
    nums_so_far = []
    for i in range(0, len(data[1])):
        residual = data[1][i] - (a + b * data[0][i])
        nums_so_far.append(residual)

    return nums_so_far


def residual_standard_deviation(residual_list: list):
    """ Return the standard deviation of the residual values.
    """
    squared_residuals = [residual ** 2 for residual in residual_list]
    standard_dev = math.sqrt(sum(squared_residuals) / (len(squared_residuals) - 2))
    return standard_dev


def prediction_interval_sigma(standard_dev: float) -> float:
    """ Return the +- value of an 80% prediction interval.
    """
    return standard_dev * 1.28


def multiple_regression2(red_list_data: tuple, dataset1: tuple, dataset2: tuple, change1: float, change2: float) -> float:
    """ Return the prediction of a multiple linear regression with three variables
    """
    y = pandas.DataFrame(red_list_data[1])
    x = pandas.DataFrame(list(zip(dataset1[1], dataset2[1])))
    linear_regression = LinearRegression()
    linear_regression.fit(x, y)
    y_pred = linear_regression.predict([[dataset1[1][-1] + change1, dataset2[1][-1] + change2]])
    return float(y_pred)


def multiple_regression3(red_list_data: tuple, dataset1: tuple, dataset2: tuple, dataset3: tuple, change1: float, change2: float, change3: float) -> float:
    """ Return the prediction of a multiple linear regression with three variables
    """
    y = pandas.DataFrame(red_list_data[1])
    x = pandas.DataFrame(list(zip(dataset1[1], dataset2[1], dataset3[1])))
    linear_regression = LinearRegression()
    linear_regression.fit(x, y)
    y_pred = linear_regression.predict([[dataset1[1][-1] + change1, dataset2[1][-1] + change2, dataset3[1][-1] + change3]])
    return float(y_pred)
