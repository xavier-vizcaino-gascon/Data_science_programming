"""
Main tools for dictionaries creation and manipulation
"""
import concurrent.futures

import pandas as pd


def players_dict(df: pd.DataFrame, ids: list, cols: list) -> dict:
    """
    This function creates a dictionary with the information contained in a dataframe

    param df: dataframe
    param ids: list of player identifier
    param cols: requested information columns
    return: dictionary with the following format:
        + key = player identifier
        + values = dict with the following format:
            + key = column_id from cols list
            + Values = list of values in dataframe for the given column_id
    """
    cols_t: list = cols.copy()
    if "sofifa_id" not in cols_t:
        cols_t.append("sofifa_id")

    if "sofifa_id" in cols_t:
        # Dataframe subset
        df = df.loc[:, cols_t]
        cols_t.remove("sofifa_id")

    result: dict = {}

    for ide in ids:
        df_t: pd.DataFrame = df[df["sofifa_id"] == ide]
        df_t.pop("sofifa_id")
        result[ide] = df_t.to_dict("list")
    return result


def players_dict_futures(df: pd.DataFrame, ids: list, cols: list) -> dict:
    """
    This function creates a dictionary with the information contained in a dataframe
    through concurrency (multithreading)

    param df: dataframe
    param ids: list of player identifier
    param cols: requested information columns
    return: dictionary with the following format:
        + key = player identifier
        + values = dict with the following format:
            + key = column_id from cols list
            + Values = list of values in dataframe for the given column_id
    """

    def create_dict(df_f: pd.DataFrame, ide_f: int) -> dict:
        """
        This function creates a dictionary with all the information from
        the given dataframe

        param df_f: subset dataframe with the requested columns
        param ide_f: player identifier
        return: dict with the following format:
            + key = column_id from cols list
            + Values = list of values in dataframe for the given column_id
        """
        df_t: pd.DataFrame = df_f[df_f["sofifa_id"] == ide_f]
        df_t.pop("sofifa_id")
        return df_t.to_dict("list")

    cols_t: list = cols.copy()
    if "sofifa_id" not in cols_t:
        cols_t.append("sofifa_id")

    if "sofifa_id" in cols_t:
        df = df.loc[:, cols_t]
        cols_t.remove("sofifa_id")

    result: dict = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_thread = {executor.submit(create_dict, df, ide): ide for ide in ids}
        for future in concurrent.futures.as_completed(future_thread):
            try:
                result[future_thread[future]] = future.result()
            except Exception as exc:
                print('%s generated an exception: %s' % (future_thread[future], exc))
    return result


def clean_player_dict(player_dict: dict, col_query: list) -> dict:
    """
    This function clears dictionaries up removing duplicates according to queries

    param player_dict: rough dictionary
    param col_query: list of tuples with the following format:
        + 0: column name
        + 1: operation to perform. Accepted commands are:
            + "one": the first value of the list is removed
            + "del_rep": repetitions are removed
    return: a clean dictionary
    """
    for item in col_query:
        key: str = item[0]
        value: str = item[1]
        if value == "one":
            player_dict[key] = player_dict[key][0]
        elif value == "del_rep":
            temp: list = list(set(player_dict[key]))
            if any("," in elem for elem in temp):
                flat: list = [x.strip() for x in temp for x in x.split(",")]
                player_dict[key] = list(set(flat))
            else:
                player_dict[key] = temp
        else:
            raise ValueError("Filter type = {}, not found".format(item[1]))
    return player_dict


def clean_up_players_dict(multi_dict: dict, col_query: list) -> dict:
    """
    This function performs iteration along all items of a dictionary with
    multiple players calling clean_player_dict, for sub-dictionary cleaning
    operations

    param players_dict: dictionary with information from multiple players
    param col_query: queries list to pass for cleaning
    return: clean multi-player dictionary
    """
    for key in multi_dict.keys():
        clean_player_dict(multi_dict[key], col_query)
    return multi_dict
