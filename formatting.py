import xlrd
import csv
from typing import Tuple, List, Any

# Usable data
#
# This is in the form of Tuple[datetime.datetime, List[Any]]
# (start_year, [value1, value2, value3, value4])
#
# Each element in the list happens on the year later.


def xlsx_to_data(filename: str) -> Tuple[int, List[Any]]:
    """ Convert the xlsx file to usable data.
    """
    # TODO: Implement your function here.


def csv_to_data(filename: str) -> Tuple[int, List[Any]]:
    """ Convert the csv file to usable data.
    """
    # TODO: Implement your function here.
