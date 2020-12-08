import xlrd
import csv
from typing import Tuple, List, Any

# Usable data
#
# This is in the form of Tuple[datetime.datetime, List[Any]]
# (start_year, [value1, value2, value3, value4])
#
# Each element in the list happens on the year later.

def xlsx_to_data(filename: str) -> Any:#Tuple[int, List[Any]]:
    """ Convert the xlsx file to usable data.
    """
    workbook = xlrd.open_workbook('data/red_list_data.xlsx')
    second_sheet = workbook.sheet_by_index(1)

    data_so_far = {}
    for i in range(3, second_sheet.nrows):
        for j in range(1, second_sheet.ncols):
            if j == 1:
                data_so_far[second_sheet.cell(i, 0).value] = [second_sheet.cell(i, j).value]
            else:
                data_so_far[second_sheet.cell(i, 0).value].append(second_sheet.cell(i, j).value)

    return data_so_far


def csv_to_data(filename: str) -> Tuple[int, List[Any]]:
    """ Convert the csv file to usable data.
    """
    # TODO: Implement your function here.
