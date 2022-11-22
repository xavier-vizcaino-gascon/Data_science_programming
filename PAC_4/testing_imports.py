# pylint: skip-file
import pandas as pd
import os
from utils.preprocess.preprocess import read_add_year_gender, join_male_female, join_datasets_year
from utils.statistics.basic_statistics import find_max_col, find_rows_query
from utils.statistics.bmi_statistics import calculate_bmi
from utils.datamanagement.dictionaries import players_dict, clean_up_players_dict
from utils.datamanagement.evolution import top_average_column, consistency_check
from utils.datamanagement.rosters import all_candidates, top_candidates, all_roster, roster_skills
