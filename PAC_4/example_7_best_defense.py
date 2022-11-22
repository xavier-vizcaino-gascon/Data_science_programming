"""
This example calculates the best defense roster for gender male and young players,
gender female and young players & senior players (male & female)
"""
import pandas as pd

from utils.preprocess import preprocess as prep
from utils.datamanagement.evolution import consistency_check
from utils.datamanagement.rosters import all_candidates, top_candidates, all_roster, roster_skills

# SETTINGS
# General
DATA_FOLDER: str = "data"
YEAR_LIST: list = list(range(2016, 2022 + 1))

# Roster
PLAYER_POSITIONS: list = ["LB", "CB", "RB"]

# Initial filtering
FILTERS: list = [(["gender", "league_level", "age", "defending"], ["M", (0, 1), (0, 28), (75, 100)]),
                 (["gender", "age", "defending"], ["F", (0, 28), (75, 100)]),
                 (["age", "defending"], [(30, 50), (75, 100)])]

# Views & queries
VIEW: list = ["sofifa_id", "short_name", "year", "gender", "age", "player_positions",
              "club_name", "overall", "potential", "defending",
              "skill_long_passing", "skill_ball_control", "mentality_interceptions",
              "mentality_positioning", "defending_marking_awareness",
              "defending_standing_tackle", "defending_sliding_tackle"]
COL_Q: list = [("short_name", "one"), ("gender", "one"),
               ("player_positions", "del_rep")]

# Top skills
SKILLS: list = ["overall", "potential", "defending",
                "skill_long_passing", "skill_ball_control",
                "movement_reactions", "movement_sprint_speed",
                "mentality_interceptions", "mentality_positioning",
                "defending_marking_awareness", "defending_standing_tackle",
                "defending_sliding_tackle"]

THRESHOLD = 2
TOP_PLAYERS = 20


# OPERATIONS
# Check input data consistency
consistency_check(VIEW, SKILLS)

# Load data
data: pd.DataFrame = prep.join_datasets_year(DATA_FOLDER, YEAR_LIST)

for i in range(3):
    # Data filtering & management
    ROSTER = all_candidates(PLAYER_POSITIONS, FILTERS[i], data, VIEW, COL_Q)

    # Top X players in skills
    ROSTER_TOP = top_candidates(ROSTER, SKILLS, THRESHOLD, TOP_PLAYERS)

    # All possible roster
    ROSTERS = all_roster(ROSTER_TOP)

    # Remove rosters with duplicated players while calculating total roster_skills
    FINAL_ROSTERS = [(x, roster_skills(x, ROSTER_TOP)) for x in ROSTERS if len(set(x)) == 4]

    # Sort rosters by total roster_skills value
    FINAL_ROSTERS.sort(key=lambda tup: tup[1], reverse=True)
    if i == 0:
        print("\n** Male defense **")
        print("Best male defense roster is {} with a global roster skill value of {}".
              format(FINAL_ROSTERS[0][0], round(FINAL_ROSTERS[0][1], 1)))
    elif i == 1:
        print("\n** Female defense **")
        print("Best female defense roster is {} with a global roster skill value of {}".
              format(FINAL_ROSTERS[0][0], round(FINAL_ROSTERS[0][1], 1)))
    elif i == 2:
        print("\n** Senior defense **")
        print("Best senior defense roster is {} with a global roster skill value of {}".
              format(FINAL_ROSTERS[0][0], round(FINAL_ROSTERS[0][1], 1)))
    else:
        raise ValueError("Iterator overflow")
