
import formatting
import computing
import graphing
from typing import *


def run(selected: List[bool], interval_increases: List[float]) -> None:
    # Formatted data
    red_list_data = formatting.xlsx_to_data("data//red_list_data.xlsx")
    formatting.add_red_list_species(red_list_data)
    red_list_data = formatting.dict_to_tuple_of_lists(red_list_data)

    if selected.count(True) == 1:
        if selected[0]:  # assuming only one is true
            temperature_data = formatting.csv_to_data("data//global_land_temperatures.csv")
            computing.average_temperature_data(temperature_data)
            comparison_data = formatting.dict_to_tuple_of_lists(temperature_data)
            computing.same_year(red_list_data, True)
            change = interval_increases[0]
        elif selected[1]:
            natural_disasters_data = formatting.csv_to_data("data//natural_disasters_data.csv")
            comparison_data = formatting.dict_to_tuple_of_lists(natural_disasters_data)
            change = interval_increases[1]
        else:
            carbon_data = formatting.xlsx_to_data("data//carbon_dioxide_concentrations.xlsx")
            comparison_data = formatting.dict_to_tuple_of_lists(carbon_data)
            change = interval_increases[2]

        comparison_data = computing.same_year(comparison_data, False)

        years = red_list_data[0]
        dep_val = red_list_data[1]
        indep_val = comparison_data[1]
        a, b = computing.simple_linear_regression((indep_val, dep_val))
        future_value = computing.predict_future_value(a, b, indep_val, change)
        residuals = computing.residuals((indep_val, dep_val), a, b)
        standard_dev = computing.residual_standard_deviation(residuals)
        sigma = computing.prediction_interval_sigma(standard_dev)

        new_point_x = [indep_val[-1] + change]
        new_point_y = [future_value]
        xmax = (indep_val[-1] + change) + 0.1 * (indep_val[-1] + change - indep_val[0])
        xmin = indep_val[0] - 0.1 * (indep_val[-1] - indep_val[0])
        graphing.plot_datasets(years, dep_val, [('Temperature', indep_val)], a, b, xmax, xmin, new_point_x, new_point_y, sigma)

    # else:
    #     temperature_data, natural_disasters_data, carbon_data = [], [], []
    #     condition = False
    #     if selected[0]:  # assuming only one is true
    #         condition = True
    #         temperature_data = formatting.csv_to_data("data//global_land_temperatures.csv")
    #         computing.average_temperature_data(temperature_data)
    #         temperature_data = formatting.dict_to_tuple_of_lists(temperature_data)
    #         temperature_data = computing.same_year(temperature_data, condition)
    #         change1 = interval_increases[0]
    #     if selected[1]:
    #         natural_disasters_data = formatting.csv_to_data("data//natural_disasters_data.csv")
    #         natural_disasters_data = formatting.dict_to_tuple_of_lists(natural_disasters_data)
    #         natural_disasters_data = computing.same_year(natural_disasters_data, condition)
    #         change2 = interval_increases[1]
    #     if selected[2]:
    #         carbon_data = formatting.xlsx_to_data("data//carbon_dioxide_concentrations.xlsx")
    #         carbon_data = formatting.dict_to_tuple_of_lists(carbon_data)
    #         carbon_data = computing.same_year(carbon_data, condition)
    #         change3 = interval_increases[2]
    #
    #
    #     years = red_list_data[0]
    #     future_value = computing.multiple_regression(red_list_data, temperature_data, carbon_data, natural_disasters_data)


def run_with_gui() -> None:
    """ Runs with graphical interface
    """
    import interface


