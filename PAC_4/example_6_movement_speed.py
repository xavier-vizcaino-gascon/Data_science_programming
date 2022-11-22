"""
This example provides the evolution of "movement_sprint_speed" of the four
best average of this characteristic.
"""
import pprint

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

from utils.statistics import basic_statistics as bstat
from utils.datamanagement import evolution as evo
from utils.preprocess import preprocess as prep
from utils.datamanagement.dictionaries import players_dict_futures, clean_up_players_dict

mpl.use("TkAgg")

# Data source
DATA_FOLDER: str = "data"
YEAR_LIST: list = list(range(2016, 2022 + 1))

# Load data
data: pd.DataFrame = prep.join_datasets_year(DATA_FOLDER, YEAR_LIST)

# Get id list from data where movement_sprint_speed >= 85
FILTERS: tuple = (["movement_sprint_speed"], [(85, 200)])
VIEW: list = ["sofifa_id", "movement_sprint_speed"]

fast_players: pd.DataFrame = bstat.find_rows_query(data, FILTERS, VIEW)
id_list: list = list(set(fast_players["sofifa_id"].to_list()))

# Dictionary building
COL_LIST: list = ["short_name", "movement_sprint_speed", "year"]
players_info: dict = players_dict_futures(data, id_list, COL_LIST)

# Dictionary cleaning
COL_Q: list = [("short_name", "one")]
clean_players_info: dict = clean_up_players_dict(players_info, COL_Q)

# Evolution check
THRESHOLD: int = 4
result: list = evo.top_average_column(clean_players_info, "short_name",
                                      "movement_sprint_speed", THRESHOLD)
result: list = result[0:4]
print("\n** Movement speed **")
pprint.pprint(result)

# Chart
plt.plot(result[0][2]["year"], result[0][2]["value"], label=result[0][0])
plt.plot(result[1][2]["year"], result[1][2]["value"], label=result[1][0])
plt.plot(result[2][2]["year"], result[2][2]["value"], label=result[2][0])
plt.plot(result[3][2]["year"], result[3][2]["value"], label=result[3][0])
plt.title("movement_sprint_speed evolution")
plt.xlabel("years")
plt.ylabel("movement_sprint_speed")
plt.legend()
plt.show()
