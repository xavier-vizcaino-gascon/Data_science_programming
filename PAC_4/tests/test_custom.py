# pylint: skip-file
import unittest

from HTMLTestRunner import HTMLTestRunner

from testing_imports import *


class CustomTestsEx2(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.data = join_datasets_year("data", [2016])

    def test_custom_ex2a(self):
        # Check if dimensions are correct
        filtered_df = find_max_col(self.data, "potential", ["short_name", "potential"])
        # Check output shapes
        self.assertEqual(filtered_df.shape[1], 2)
        filtered_df = find_max_col(self.data, "age", ["age"])
        self.assertEqual(filtered_df.shape[0], 2)


class CustomTestsEx3(unittest.TestCase):

    @classmethod
    def setUp(cls):
        # Create some fake data
        cls.data = pd.DataFrame({"short_name": ["L. Messi", "A. Putellas", "A. Hegerberg"],
                                 "gender": ["M", "F", "F"],
                                 "year": [2021, 2021, 2022],
                                 "height_cm": [169, 171, 177],
                                 "weight_kg": [67, 66, 70]})

    def test_custom_ex3a(self):
        female_bmi = calculate_bmi(self.data, "F", 2021, ["short_name"])
        # Check if calculate_bmi works for women
        self.assertEqual(female_bmi["short_name"].iloc[0], "A. Putellas")
        self.assertEqual(female_bmi["BMI"].iloc[0], 66 / (1.71 * 1.71))


class CustomTestsEx4(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.data = join_datasets_year("data", [2016, 2017, 2018])

    def test_custom_ex4b(self):
        ids = [176580, 168542]
        columns_of_interest = ["overall", "potential"]
        data_dict = players_dict(self.data, ids, columns_of_interest)
        data_dict = clean_up_players_dict(data_dict, [("potential", "one")])
        # Check
        self.assertEqual(data_dict[168542]["potential"], 88)


class CustomTestsEx6(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.data = join_datasets_year("data", list(range(2016, 2022 + 1)))

    def test_custom_ex6(self):
        PLAYER_POSITIONS = ["LB", "CB", "RB"]
        FILTERS = (["gender", "league_level", "club_name", "age", "defending"],
                   ["M", (0, 1), "FC Barcelona", (0, 50), (0, 100)])
        VIEW = ["sofifa_id", "short_name", "year", "gender", "age", "player_positions",
                      "club_name", "overall", "potential", "defending",
                      "skill_long_passing", "skill_ball_control", "mentality_interceptions",
                      "mentality_positioning", "defending_marking_awareness",
                      "defending_standing_tackle", "defending_sliding_tackle"]
        COL_Q = [("short_name", "one"), ("gender", "one"),
                       ("player_positions", "del_rep")]
        SKILLS = ["overall", "potential", "defending",
                        "skill_long_passing", "skill_ball_control",
                        "movement_reactions", "movement_sprint_speed",
                        "mentality_interceptions", "mentality_positioning",
                        "defending_marking_awareness", "defending_standing_tackle",
                        "defending_sliding_tackle"]
        THRESHOLD = 2
        TOP_PLAYERS = 5
        consistency_check(VIEW, SKILLS)

        ROSTER = all_candidates(PLAYER_POSITIONS, FILTERS, self.data, VIEW, COL_Q)
        ROSTER_TOP = top_candidates(ROSTER, SKILLS, THRESHOLD, TOP_PLAYERS)
        ROSTERS = all_roster(ROSTER_TOP)
        FINAL_ROSTERS = [(x, roster_skills(x, ROSTER_TOP)) for x in ROSTERS if len(set(x)) == 4]
        FINAL_ROSTERS.sort(key=lambda tup: tup[1], reverse=True)

        # Check
        self.assertEqual(FINAL_ROSTERS[0][0], ('Jordi Alba', 'J. Mascherano', 'Piqué', 'Nélson Semedo'))


if __name__ == '__main__':
    suite = unittest.TestSuite()

    suite.addTest(unittest.makeSuite(CustomTestsEx2))
    suite.addTest(unittest.makeSuite(CustomTestsEx3))
    suite.addTest(unittest.makeSuite(CustomTestsEx4))
    suite.addTest(unittest.makeSuite(CustomTestsEx6))

    runner = HTMLTestRunner(log=True, verbosity=2, output='reports',
                            title='PAC4', description='PAC4 custom tests',
                            report_name='Custom tests')
    runner.run(suite)
