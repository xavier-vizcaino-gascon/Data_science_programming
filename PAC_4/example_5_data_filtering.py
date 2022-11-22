"""
This example creates a dictionary with players info and later
cleans the dictionary according to col_query information
"""
import pprint

import pandas as pd

from utils.preprocess import preprocess as prep
from utils.datamanagement.dictionaries import players_dict, clean_up_players_dict

# Data source
DATA_FOLDER: str = "data"
YEAR_LIST: list = list(range(2016, 2018 + 1))

# Settings
ID_LIST: list = [226328, 192476, 230566]
COL_LIST: list = ["short_name", "overall", "potential", "player_positions", "year"]
COL_Q: list = [("player_positions", "del_rep"), ("short_name", "one")]

# Load data
data: pd.DataFrame = prep.join_datasets_year(DATA_FOLDER, YEAR_LIST)

# Dictionary building
players_info: dict = players_dict(data, ID_LIST, COL_LIST)
print("\n** General dictionary **")
pprint.pprint(players_info)

# Dictionary cleaning
clean_players_info: dict = clean_up_players_dict(players_info, COL_Q)
print("\n** Filtered dictionary **")
pprint.pprint(clean_players_info)
