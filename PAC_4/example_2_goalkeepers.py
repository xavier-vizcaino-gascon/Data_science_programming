""" This example prints:
- Short name,  year, age, overall, potential of all:
* Goalkeepers, female, older than 28 with overall higher than 85
"""

import pandas as pd

import utils.statistics.basic_statistics as bstat
from utils.preprocess import preprocess as prep

# General settings
DATA_FOLDER = "data"
YEAR_LIST = list(range(2016, 2022 + 1))

# Load data
data: pd.DataFrame = prep.join_datasets_year(DATA_FOLDER, YEAR_LIST)

FILTERS = (["gender", "player_positions", "age", "overall"],
           ["F", "GK", (28 + 1, 200), (85 + 1, 200)])
VIEW = ["short_name", "year", "age", "overall", "potential"]

# Advanced filter
goalkeepers: pd.DataFrame = bstat.find_rows_query(data, FILTERS, VIEW)
print("\n** Female goalkeepers **")
print(goalkeepers)
