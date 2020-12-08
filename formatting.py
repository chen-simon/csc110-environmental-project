import xlrd
import csv
from typing import Tuple, List, Any, Dict

# Usable data
#
# This is in the form of Tuple[datetime.datetime, List[Any]]
# (start_year, [value1, value2, value3, value4])
#
# Each element in the list happens on the year later.

def xlsx_to_data(filename: str) -> Dict[str, List[int]]:
    """ Convert the xlsx file to usable data.
    """
    workbook = xlrd.open_workbook(filename)
    second_sheet = workbook.sheet_by_index(1)

    data_so_far = {}
    for i in range(3, second_sheet.nrows):
        data_so_far[second_sheet.cell(i, 0).value] = []
        for j in range(1, second_sheet.ncols):
            if isinstance(second_sheet.cell(i, j).value, (int, float)):
                data_so_far[second_sheet.cell(i, 0).value].append(second_sheet.cell(i, j).value)

    return data_so_far


def csv_to_data(filename: str) -> Tuple[int, List[Any]]:
    """ Convert the csv file to usable data.
    """
    # TODO: Implement your function here.
