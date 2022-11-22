"""
Main tools for roster management
"""
import collections
import itertools
from collections import Counter

import pandas as pd

from utils.statistics import basic_statistics as bstat
from utils.datamanagement import evolution as evo
from utils.datamanagement.dictionaries import players_dict_futures, clean_up_players_dict


def all_candidates(player_positions: list, filters: tuple,
                   data: pd.DataFrame, view: list, col_q: list) -> dict:
    """
    This function generates a dictionary with all possible candidates
    that fulfill the filtering conditions.

    param player_positions: positions to be considered in the roster
    param filters: filters to be applied in the complete data_frame
    param data: data_frame with all data
    param view: column variables to be included in the return dictionary
    param col_q: queries for dictionary cleaning
    return: returns a dictionary with the following structure:
        + key: position
        + values: dictionary with the following structure:
            + key: player_id
            + values: dict with the following structure:
                + key: column id or characteristic
                + values: list of values for that column or characteristic
    """
    roster: dict = {}
    for position in player_positions:
        filters[0].append("player_positions")
        filters[1].append(position)
        position_df: pd.DataFrame = bstat.find_rows_query(data, filters, view)
        players_info: dict = players_dict_futures(position_df,
                                                  position_df["sofifa_id"].unique(),
                                                  view)
        clean_players_info: dict = clean_up_players_dict(players_info, col_q)
        roster[position] = clean_players_info
        filters[0].remove("player_positions")
        filters[1].remove(position)
    return roster


def top_candidates(roster: dict, skills: list, threshold: int, top_players: int) -> dict:
    """

    param roster:
    param skills:
    param threshold:
    param top_players:
    return: a dictionary with the following format:
        + key: points / skills / skills_dict / candidates
        + values:
            - for k=points, list of tuples with the following format:
                + 0: player_id
                + 1: Sum of total skill position points for the given
                player (position points are based on the player's position
                ranking of each skill, taking "top_players" points for a
                given skill when the player is at the 1st position,
                "top_players"-1 when is 2nd, and so on
            - for k=skills, list of tuples with the following format:
                + 0: player_id
                + 1: Sum of total skill value for the given player
            - for k=skills_dict, dict version of skills information
            - for k=candidates, list of players that are in top global position
    """
    roster_top: dict = {}
    for key in roster.keys():
        roster_top[key] = {}
        flat_list: list = []
        for skill_id in skills:
            result: list = evo.top_average_column(roster[key], "short_name", skill_id, threshold)
            result: list = result[0:top_players]
            for i, val in enumerate(result):
                pos_score = position_scoring(i, top_players)
                flat_list.append((val[0], pos_score, val[1]))
        # Skills value & list position totalization by player
        tsps: collections.Counter = Counter()
        tsv: collections.Counter = Counter()
        for k, v, z in flat_list:
            tsps[k] += v
            tsv[k] += z
        roster_top[key]["points"] = tsps.most_common()
        roster_top[key]["skills"] = tsv.most_common()
        roster_top[key]["skills_dict"] = dict(tsv.most_common())
        unzipped: zip = zip(*tsps.most_common())
        if key != "CB":
            roster_top[key]["candidates"] = list(list(unzipped)[0])[0:int(top_players / 2)]
        else:
            roster_top[key]["candidates"] = list(list(unzipped)[0])[0:top_players]
    return roster_top


def all_roster(roster_top: dict) -> list:
    """
    This function receives information from the returned roster_top dictionary and generates a list
    with all possible roster combinations.

    param roster_top: dictionary
    return: list of tuples, where each tuple contains 4 player ids positioned according to their
    field position:
        + (LB, CB, CB, RB)
    """
    all_list: list = []
    for key in roster_top.keys():
        all_list.append(roster_top[key]["candidates"])
        if key == "CB":
            all_list.append(roster_top[key]["candidates"])
    return list(itertools.product(*all_list))


def roster_skills(x: tuple, di: dict) -> float:
    """
    This calculates the total roster skill value

    param x: tuple with the roster
    param di: dictionary with information about position, player_id and total skills
    return: total skill value
    """
    p_lb: float = di["LB"]["skills_dict"][x[0]]
    p_cb1: float = di["CB"]["skills_dict"][x[1]]
    p_cb2: float = di["CB"]["skills_dict"][x[2]]
    p_rb: float = di["RB"]["skills_dict"][x[3]]
    return p_lb + p_cb1 + p_cb2 + p_rb


def position_scoring(pos: int, total: int) -> int:
    """
    This function calculates the scoring value according to the position in top list
    param pos: position in top list
    param total: total number of top players
    return: the difference between both values, as it is considered the related
    scoring
    """
    return total-pos
