"""
This example creates one bar chart with the maximum BMI by country
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

import utils.statistics.bmi_statistics as bmistat
from utils.other.other import clean_url
from utils.preprocess import preprocess as prep

mpl.use("TkAgg")

# General settings
DATA_FOLDER = "data"
YEAR_LIST = list(range(2016, 2022 + 1))
VIEW = ["gender", "year", "club_flag_url", "height_cm", "weight_kg"]

# Load data
data: pd.DataFrame = prep.join_datasets_year(DATA_FOLDER, YEAR_LIST)

# Extract BMI
ALL_BMI = bmistat.calculate_bmi(data, "M", 2022, VIEW)

# Group by country & get group max
FLAG_BMI_MAX = ALL_BMI.groupby(["club_flag_url"]).max()
FLAG_BMI_MAX = clean_url(FLAG_BMI_MAX, "club_flag_url")

# Generate chart
FIG, AX = plt.subplots()
FIG.set_size_inches(15, 10)
AX.bar(FLAG_BMI_MAX["club_flag_url"], FLAG_BMI_MAX["BMI"])
AX.set_xlabel("countries")
AX.set_ylabel("BMI")
AX.set_title("BMI vs countries")
AX.tick_params(axis="x", labelrotation=90)
plt.show()
