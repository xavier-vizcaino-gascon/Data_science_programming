"""
General tools and utils
"""
import re

import numpy as np
import pandas as pd


def clean_url(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    This function applies country code extraction along a column of dataframe

    param df: dataframe
    param col: column with url
    return: dataframe with column url modified to report only the country code.
    """
    def last_part(row, column) -> str:
        """
        This function extracts the country code from a URL

        param row: dataframe row
        param column: column with the url
        return: given url such as "https://cdn.sofifa.net/flags/ar.png" this function returns
        "ar" as string.
        """
        temp = row[column]
        temp = temp.split("/")
        temp = temp[len(temp)-1]
        temp = temp.split(".")[0]
        return temp

    # create copy to avoid SettingWithCopyWarning
    df = df.copy()
    df.reset_index(inplace=True)
    df.loc[:, col] = df.apply(last_part, axis=1, column=col)
    return df


def del_text_parenthesis(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    This function applies parenthesis removal along a column of the dataframe

    :param df: dataframe
    :param col: column where to remove parenthesis
    :return: dataframe with column "col" converted
    """
    def rm_parenthesis(row, column: str):
        """
        This function substitutes parenthesis for ""

        :param row: dataframe row
        :param column: column where to remove parenthesis
        :return: initial string without parenthesis
        """
        return re.sub(r' \([^)]*\)', "", row[column])

    # create copy to avoid SettingWithCopyWarning
    df = df.copy()
    df.loc[:, col] = df.apply(rm_parenthesis, column=col, axis=1)
    return df


def colorin(labels: np.ndarray):
    """
    This function generates an array with color ids for
    Matplotlib according to the order of the inputs.
    Therefore, charts with same variables in different
    order will be comparable.

    param labels:
    return: array with colors
    """
    color_dict = {"Underweight": "tab:orange",
                  "Normal weight": "tab:green",
                  "Overweight": "tab:blue",
                  "Obesity": "tab:red"
                  }
    out_list: list = [color_dict[key] for key in labels.tolist()]
    return np.array(out_list)
