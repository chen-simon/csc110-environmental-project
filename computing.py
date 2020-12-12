from typing import Tuple, List, Dict


def average_temperature_data(data: Dict[int, List[float]]) -> None:
    """ Calculate average temperature during each year. This function mutates the input data.

    The dictionary changes from the form Dict[int, List[float]] to Dict[int, float]
    upon mutation.
    """
    for key in data:
        data[key] = sum(data[key]) / len(data[key])

