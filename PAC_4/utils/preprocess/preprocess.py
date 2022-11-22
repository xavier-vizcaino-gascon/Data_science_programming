"""
Main tools for data preprocessing
"""
import os

import pandas as pd


def read_add_year_gender(filepath: str, gender: str, year: int) -> pd.DataFrame:
    """
    This function reads a .csv file, creates Pandas dataframe and adds two
    new columns named:
        + gender
        + year
    New columns are filled with the values from input parameters.

    param filepath: filepath (str) to the .csvfile.
    param gender: value (str) to fill into gender column.
    param year: value (int) to fill into year column.
    return: pandas dataframe with loaded data + 2 new columns.
    """
    df = pd.read_csv(filepath, dtype={'nation_position': str, 'lw': str, 'lf': str,
                                      'cf': str, 'rf': str, 'rw': str, 'gk': str,
                                      'nation_logo_url': str})
    df["gender"] = gender
    df["year"] = year
    return df


def join_male_female(path: str, year: int) -> pd.DataFrame:
    """
    This function looks for all the files with its name ending
    with the input date (year in file name is %YY format,
    while function input is in %YYYY format) and performs
    dataframe concatenation.

    This function also checks if the file starts with "female".

    These two checks (year & gender) are useful to call read
    procedures during preprocessing and properly identify
    datasets.

    param path: path (str) to data files.
    param year: year (int) to gather data and concatenate.
    required year format  = %YYYY
    return: dataframe with all data from a given year.
    """

    df = pd.DataFrame()
    for filename in os.listdir(path):
        if "players" in filename:
            if int(filename[-6:][0:2]) == year-2000:
                gender = "F" if (filename[0:6] == "female") else "M"
                file = os.path.join(path, filename)
                df = pd.concat([df, read_add_year_gender(file, gender, year)], axis=0)

    return df


def join_datasets_year(path: str, years: list) -> pd.DataFrame:
    """
    This function iterates over a list of years and concatenates
    dataframes related to listed years into a bigger dataframe

    param path: path (str) to data files
    param years: years to get data and concatenate (list of integers,
    with format %YYYY)
    return: a dataframe containing all infor for given years.
    """
    if not os.path.isdir(path):
        raise TypeError("Data folder {} does not exist".format(path))

    df = pd.DataFrame()
    for year in years:
        if not 2016 <= int(year) <= 2022:
            raise ValueError("Error in year = {}\nYear must be between 2016 & 2022".format(year))
        df = pd.concat([df, join_male_female(path, int(year))], axis=0)

    return df
