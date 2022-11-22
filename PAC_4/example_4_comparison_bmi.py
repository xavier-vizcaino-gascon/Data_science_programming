"""
This example generates 2 sets of comparative pie charts:
    - Items compared are the percentage of population for each BMI category.
    - Comparison is made between players (left) and Spain population (right).
    - Comparison is performed in 2 different age groups 18-24 & 25-34.
"""
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from utils.statistics import basic_statistics as bstat
from utils.statistics import bmi_statistics as bmistat
from utils.other.other import colorin
from utils.other.other import del_text_parenthesis as dtp
from utils.preprocess import preprocess as prep

mpl.use("TkAgg")

# PLAYERS
# Data source
DATA_FOLDER = "data"
YEAR_LIST = list(range(2016, 2022 + 1))
# Settings
FILTERS = (["age", "potential", "player_positions"],
           [(17, 35), (79, 100), "CB"])
VIEW = ["short_name", "gender", "year", "age", "height_cm", "weight_kg"]

# Load data
data: pd.DataFrame = prep.join_datasets_year(DATA_FOLDER, YEAR_LIST)

# Advanced filter
players: pd.DataFrame = bstat.find_rows_query(data, FILTERS, VIEW)

# BMI calculation
players_bmi: pd.DataFrame = bmistat.calculate_bmi(players, "M", 2020, VIEW)

# Categorical var creation
CAT_COND = [players_bmi.BMI < 18.5,
            (players_bmi.BMI >= 18.5) & (players_bmi.BMI < 25),
            (players_bmi.BMI >= 25) & (players_bmi.BMI < 30),
            players_bmi.BMI > 30]
CAT_VALUE = ["Underweight", "Normal weight", "Overweight", "Obesity"]
players_bmi["bmi_cat"] = np.select(CAT_COND, CAT_VALUE)

# Totalization
P_BMI_1824 = players_bmi[players_bmi["age"] < 25].groupby("bmi_cat").count()
P_BMI_2534 = players_bmi[players_bmi["age"] > 24].groupby("bmi_cat").count()


# SPANISH POPULATION
# Data source
INE_FILE = "ine_BMI.csv"
# Settings
VIEW = ["Adult body mass index", "Sex", "Age", "Total"]

# Load data
data_ine: pd.DataFrame = pd.read_csv(os.path.join(DATA_FOLDER, INE_FILE), sep=";", thousands=",")

# Totalization
DATA_INE_1824 = bstat.find_rows_query(data_ine,
                                      (["Sex", "Age"],
                                       ["Men", "From 18 to 24 years old"]),
                                      VIEW)
DATA_INE_2534 = bstat.find_rows_query(data_ine,
                                      (["Sex", "Age"],
                                       ["Men", "From 25 to 34 years old"]),
                                      VIEW)

# Renaming
DATA_INE_1824 = dtp(DATA_INE_1824, "Adult body mass index")
DATA_INE_2534 = dtp(DATA_INE_2534, "Adult body mass index")


# CHARTING
# Generate label arrays
LAB00 = P_BMI_1824.index.values
LAB01 = DATA_INE_1824["Adult body mass index"].to_numpy()
LAB10 = P_BMI_2534.index.values
LAB11 = DATA_INE_2534["Adult body mass index"].to_numpy()

# Generate label-dependant color palettes
COL00 = colorin(LAB00)
COL01 = colorin(LAB01)
COL10 = colorin(LAB10)
COL11 = colorin(LAB11)

# Crate multi-chart
FIG, AXS = plt.subplots(2, 2)
FIG.set_size_inches(15, 10)
FIG.suptitle("BMI comparison_male")
AXS[0, 0].pie(P_BMI_1824["BMI"], labels=LAB00, autopct='%1.1f%%', colors=COL00)
AXS[0, 0].set_title("Players 18-24 years")
AXS[0, 1].pie(DATA_INE_1824["Total"], labels=LAB01, autopct='%1.1f%%', colors=COL01)
AXS[0, 1].set_title("Spain population 18-24 years")
AXS[1, 0].pie(P_BMI_2534["BMI"], labels=LAB10, autopct='%1.1f%%', colors=COL10)
AXS[1, 0].set_title("Players 25-34 years")
AXS[1, 1].pie(DATA_INE_2534["Total"], labels=LAB11, autopct='%1.1f%%', colors=COL11)
AXS[1, 1].set_title("Spain population 25-34 years")
plt.show()
