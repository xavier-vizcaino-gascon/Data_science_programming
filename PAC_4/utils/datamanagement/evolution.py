"""
Main tools to follow-up players evolution
"""
import numpy as np


def top_average_column(data: dict, identifier: str, col: str, threshold: int) -> list:
    """
    This function calculates the average value of a given characteristic when:
        + there is more data than threshold
        + there aren't any NaN
    if one or more characteristics above are not satisfied, values are ignored.
    The function reports one list ordered according to the values of the characteristic

    param data: dictionary with the information
    param identifier: player identifier
    param col: column to be used as characteristic
    param threshold: minimum values to be considered
    return: list of tuples with the following structure:
        + 0: player identifier
        + 1: average value of characteristic
        + 2: list of values of column characteristic
        + 3: list of values of column "year"
    """
    result: list = []
    for key in data.keys():
        if (len(data[key][col]) >= threshold) & (not np.isnan(data[key][col]).any()):
            t_identifier: str = data[key][identifier]
            t_values: list = data[key][col]
            t_values_avg: np.ndarray = np.mean(t_values)
            t_year: list = data[key]["year"]
            temp: tuple = (t_identifier, t_values_avg, {"value": t_values, "year": t_year})
            result.append(temp)
    result.sort(key=lambda tup: tup[1], reverse=True)
    return result


def consistency_check(cols: list, skills: list):
    """
    This function check the consistency of input data for evolution analysis.
    When a characteristic to be considered as skill is not found in view or filter,
    this function adds the name of the column in the view/filter list.

    param cols: view/filter columns
    param skills: list of skills to be considered in the analysis
    return: updates view/filter columns list if needed
    """
    for skill in skills:
        if skill not in cols:
            cols.append(skill)
