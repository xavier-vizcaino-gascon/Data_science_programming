""" This example prints:
- Short name,  year, age, overall, potential
of all:
* Belgium players, Male, younger than 25 with maximum potential
"""

import pandas as pd

import utils.statistics.basic_statistics as bstat
from utils.preprocess import preprocess as prep

# General settings
DATA_FOLDER = "data"
YEAR_LIST = list(range(2016, 2022 + 1))

# Load data
data: pd.DataFrame = prep.join_datasets_year(DATA_FOLDER, YEAR_LIST)

FILTERS = (["gender", "nationality_name", "age"], ["M", "Belgium", (0, 25 - 1)])
VIEW = ["short_name", "year", "age", "overall", "potential"]

# Advanced filters
belgium_players: pd.DataFrame = bstat.find_rows_query(data, FILTERS, VIEW)

# Max filter
bp_max: pd.DataFrame = bstat.find_max_col(belgium_players, "potential", VIEW)
print("\n** Belgium potential **")
print(bp_max)
