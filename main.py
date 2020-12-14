"""
Main Module

This module contains the functions that are needed to run the program from start to end. Call run_with_gui() to run the
gui. Call run() to run the prediction by entering the appropriate parameters.

This file is Copyright (c) 2020 Patricia Ding, Makayla Duffus, Simon Chen.
"""
from typing import List, Tuple
import formatting
import computing
import graphing
import interface

# constants
TEMP_DATA_LABEL = 'Temperature (°C)'
DISASTERS_DATA_LABEL = 'Number of Natural Disasters'
CARBON_DATA_LABEL = 'Carbon Concentration (ppm)'


def run(select_temp: bool, select_disasters: bool, select_carbon: bool, temp_change: float, disasters_change: float,
        carbon_change: float) -> None:
    """ Runs the prediction calculations. If one variable is changed, a simple linear regression and prediction
    interval is calculated. If more than one variable is changed, a multiple linear regression is performed with
    the sklearn library. The results will be plotted in a new window.
    """
    # in case no variable is changed
    if not any([select_temp, select_disasters, select_carbon]):
        print('Nothing selected')

    # format datasets to usable data
    red_list_data = formatting.xlsx_to_data("data//red_list_data.xlsx")
    formatting.add_red_list_species(red_list_data)

    temperature_data = formatting.csv_to_data("data//global_land_temperatures.csv")
    computing.average_temperature_data(temperature_data)

    natural_disasters_data = formatting.csv_to_data("data//natural_disasters_data.csv")
    carbon_data = formatting.xlsx_to_data("data//carbon_dioxide_concentrations.xlsx")

    # edit datasets so they have the same year
    red_list_data, temperature_data, natural_disasters_data, carbon_data \
        = computing.same_year(red_list_data, temperature_data, natural_disasters_data, carbon_data)

    # reformat data from dictionary to tuple
    red_list_data = formatting.dict_to_tuple_of_lists(red_list_data)
    temperature_data = formatting.dict_to_tuple_of_lists(temperature_data)
    natural_disasters_data = formatting.dict_to_tuple_of_lists(natural_disasters_data)
    carbon_data = formatting.dict_to_tuple_of_lists(carbon_data)

    years = red_list_data[0]

    # if one variable is changed, perform simple linear regression
    if [select_temp, select_disasters, select_carbon].count(True) == 1:
        if select_temp:
            comparison_data = temperature_data
            change = temp_change
            label = TEMP_DATA_LABEL
        elif select_disasters:
            comparison_data = natural_disasters_data
            change = disasters_change
            label = DISASTERS_DATA_LABEL
        else:  # carbon concentration data
            comparison_data = carbon_data
            change = carbon_change
            label = CARBON_DATA_LABEL

        one_variable_changed(comparison_data, red_list_data, change, label)

    # for multiple regression
    else:
        carbon_value = carbon_data[1][-1] + carbon_change
        temp_value = temperature_data[1][-1] + temp_change
        disasters_value = natural_disasters_data[1][-1] + disasters_change

        # based on which variables user selected
        if select_temp and select_disasters and select_carbon:
            # predicted value
            future_value = computing.multiple_regression3(red_list_data, temperature_data,
                                                          natural_disasters_data, carbon_data, temp_value,
                                                          disasters_value, carbon_value)

            # for graphing purposes
            other_datasets = [(CARBON_DATA_LABEL, carbon_data[1], carbon_value),
                              (DISASTERS_DATA_LABEL, natural_disasters_data[1], disasters_value),
                              (TEMP_DATA_LABEL, temperature_data[1], temp_value)]

        elif select_temp and select_carbon:
            future_value = computing.multiple_regression2(red_list_data,
                                                          temperature_data, carbon_data, temp_value, carbon_value)
            other_datasets = [(TEMP_DATA_LABEL, temperature_data[1], temp_value), (CARBON_DATA_LABEL,
                                                                                   carbon_data[1], carbon_value)]

        elif select_disasters and select_carbon:
            future_value = computing.multiple_regression2(red_list_data,
                                                          carbon_data, natural_disasters_data,
                                                          carbon_value, disasters_value)
            other_datasets = [(CARBON_DATA_LABEL, carbon_data[1], carbon_value),
                              (DISASTERS_DATA_LABEL, natural_disasters_data[1], disasters_value)]

        else:
            future_value = computing.multiple_regression2(red_list_data, temperature_data,
                                                          natural_disasters_data, temp_value, disasters_value)
            other_datasets = [(TEMP_DATA_LABEL, temperature_data[1], temp_value),
                              (DISASTERS_DATA_LABEL, natural_disasters_data[1], disasters_value)]

        # create graph
        graphing.plot_datasets(years, red_list_data[1], other_datasets, 0, 0, 0, 0, [], [future_value], 0, 0)


def run_with_gui() -> None:
    """ Runs with graphical interface.
    """
    interface.run_interface()


def one_variable_changed(comparison_data: Tuple[List[int], List[float]], red_list_data: Tuple[List[int], List[float]],
                         change: float, label: str) -> None:
    """ Perform calculations and graphing operations for simple linear regression, where one variable has been changed.
    """
    # calculations
    dep_val = red_list_data[1]
    indep_val = comparison_data[1]
    # simple linear regression
    a, b = computing.simple_linear_regression((indep_val, dep_val))
    r_squared = computing.calculate_r_squared(indep_val, dep_val, a, b)
    # predicted value
    future_value = computing.predict_future_value(a, b, indep_val, change)
    # prediction interval
    residuals = computing.residuals((indep_val, dep_val), a, b)
    standard_dev = computing.residual_standard_deviation(residuals)
    sigma = computing.prediction_interval_sigma(standard_dev)

    # plotting purposes
    new_point_x = [indep_val[-1] + change]
    new_point_y = [future_value]
    xmax = (indep_val[-1] + change) + 0.1 * (indep_val[-1] + change - indep_val[0])
    xmin = indep_val[0] - 0.1 * (indep_val[-1] - indep_val[0])

    # graph the data
    graphing.plot_datasets(red_list_data[0], dep_val, [(label, indep_val, indep_val[-1] + change)], a, b, xmax, xmin,
                           new_point_x, new_point_y, sigma, r_squared)
