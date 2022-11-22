"""
Main tools for basic statistics
"""
import pandas as pd


def find_max_col(df: pd.DataFrame, filter_col: str, cols_to_return: list) -> pd.DataFrame:
    """
    This function reports as dataframe the row with the maximum value in "filter_col"
    The number of columns reported is limited by cols_to_return list.

    param df: a dataframe containing the information to process.
    param filter_col: the target column to apply MAX filtering conditions
    param cols_to_return: a list of columns to subset from the input
    return: a subset dataframe with rows == MAX (filter_col)
    """
    # max value in filter column
    max_col = max(df[filter_col])
    # row filtering: condition == max value
    df = df[df[filter_col] == max_col]
    # columns subset
    df = df.loc[:, cols_to_return]
    return df


def find_rows_query(df: pd.DataFrame, query: tuple, cols_to_return: list) -> pd.DataFrame:
    """
    This function reports as dataframe the result of advanced filtering.

    param df: a dataframe containing the information to process.
    param query: a tuple with equally long lists in tup[0] and tup[1].
      Tup[0] must contain column names
      Tup[1] must contain filtering values:
        - if categorical it must contain a string
        - if numerical it must contain a tuple with (min, max) values
    param cols_to_return: a list of columns to subset from the input
    return: a subset dataframe with rows == all queries match
    """
    for filter_col, filter_val in zip(query[0], query[1]):
        if isinstance(filter_val, str):
            df = df[df[filter_col].str.contains(filter_val, na=False)]
        elif isinstance(filter_val, tuple):
            df = df.loc[(df[filter_col] >= filter_val[0]) & (df[filter_col] <= filter_val[1])]
        else:
            raise TypeError("Query type = {} is not considered as a valid filter".
                            format(type(filter_val)))
    # columns subset
    df = df.loc[:, cols_to_return]
    return df
