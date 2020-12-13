import formatting
import computing
import graphing
from typing import *


def run(select_temp: bool, select_disasters: bool, select_carbon: bool, temp_change: float, disasters_change: float,
        carbon_change: float) -> None:
    """ Performs calculations based on input and produces a graph
    """
    # no variable selected
    if not any([select_temp, select_disasters, select_carbon]):
        print('Nothing selected')

    # Formatted data
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
        elif select_disasters:
            comparison_data = natural_disasters_data
            change = disasters_change
        else:  # carbon concentration data
            comparison_data = carbon_data
            change = carbon_change

        # all calculations for regression + graphing purposes
        dep_val = red_list_data[1]
        indep_val = comparison_data[1]
        a, b = computing.simple_linear_regression((indep_val, dep_val))
        r_squared = computing.calculate_r_squared(indep_val, dep_val, a, b)
        future_value = computing.predict_future_value(a, b, indep_val, change)
        residuals = computing.residuals((indep_val, dep_val), a, b)
        standard_dev = computing.residual_standard_deviation(residuals)
        sigma = computing.prediction_interval_sigma(standard_dev)

        new_point_x = [indep_val[-1] + change]
        new_point_y = [future_value]
        xmax = (indep_val[-1] + change) + 0.1 * (indep_val[-1] + change - indep_val[0])
        xmin = indep_val[0] - 0.1 * (indep_val[-1] - indep_val[0])
        # temperature? - ignore for now -
        # graph the data
        graphing.plot_datasets(years, dep_val, [('Temperature', indep_val)], a, b, xmax, xmin, new_point_x, new_point_y, sigma, r_squared)

    # for multiple regression
    else:
        # based on which variables user selected
        if select_temp and select_disasters:
            future_value = computing.multiple_regression2(red_list_data, temperature_data,
                                                          natural_disasters_data, temp_change, disasters_change)
        elif select_temp and select_carbon:
            future_value = computing.multiple_regression2(red_list_data,
                                                          temperature_data, carbon_data, temp_change, carbon_change)
        elif select_disasters and select_carbon:
            future_value = computing.multiple_regression2(red_list_data,
                                                          carbon_data, natural_disasters_data,
                                                          carbon_change, disasters_change)
        else:
            future_value = computing.multiple_regression3(red_list_data, temperature_data,
                                                          natural_disasters_data, carbon_data, temp_change,
                                                          disasters_change, carbon_change)

        # predicted value
        print(future_value)


def run_with_gui() -> None:
    """ Runs with graphical interface
    """
    import interface
