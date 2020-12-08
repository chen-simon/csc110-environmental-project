from datetime import datetime

import xlrd
import csv
from typing import Tuple, List, Dict

# Usable data
#
# This is in the form of Tuple[datetime.datetime, List[Any]]
# (start_year, [value1, value2, value3, value4])
#
# Each element in the list happens on the year later.

def xlsx_to_data(filename: str) -> Dict[str, List[int]]:
    """ Convert the xlsx file to usable data.
    """
    # ------------------------------------------------------ red list data has a date - 1996/1998 that cannot be stored as an int
    # ------------------------------------------------------ for now the dates are stored as strings
    # opening workbook and accessing the 2nd sheet
    workbook = xlrd.open_workbook(filename)
    second_sheet = workbook.sheet_by_index(1)

    # ACCUMULATOR: stores the data extracted from the xlsx file
    data_so_far = {}

    # iterating through rows
    for i in range(3, second_sheet.nrows):
        # determine if it is necessary for the corresponding value to be a list
        if second_sheet.ncols > 2:
            data_so_far[second_sheet.cell(i, 0).value] = []
        # iterating through columns
        for j in range(1, second_sheet.ncols):
            # if the corresponding value is a list
            if second_sheet.ncols > 2 and isinstance(second_sheet.cell(i, j).value, (int, float)):
                data_so_far[second_sheet.cell(i, 0).value].append(second_sheet.cell(i, j).value)
            # if the corresponding value is just a number
            elif isinstance(second_sheet.cell(i, j).value, (int, float)):
                data_so_far[second_sheet.cell(i, 0).value] = second_sheet.cell(i, j).value

    return data_so_far


def csv_to_data(filename: str) -> Dict[str, float]:
    """ Convert the csv file to usable data.
    """
    # ------------------------------------------------------ temperature data is stored in yyyy-mm-dd format while natural disaster data stored in yyyy format
    # ------------------------------------------------------ for now the dates are stored as strings
    with open(filename) as file:
        reader = csv.reader(file)
        # skip the first line
        next(reader)
        # ACCUMULATOR: stores the data extracted from the csv file
        data_so_far = {}
        for row in reader:
            if row[1] != '':
                data_so_far[row[0]] = float(row[1])

    return data_so_far
