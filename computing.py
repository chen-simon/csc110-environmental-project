def average_temperature_data(data: dict) -> None:
    """ Calculate average temperature during each year. This function mutates the input data.
    """
    for key in data:
        data[key] = sum(data[key]) / len(data[key])
