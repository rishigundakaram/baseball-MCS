import unittest
from collections import defaultdict


# Assuming your Standings class is in a module named standings_module
from schedule import Schedule, Standings, default_standings, MLBTeams
from game import BaseballGame
from sim import RandomSimulator, EloSimulator
from stats import Analyzer


class TestStandings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Mock data for MLBTeams
        cls.MLBTeams = MLBTeams

    def setUp(self):
        self.standings = Standings()

    def test_init_standings(self):
        self.assertIn("AL", self.standings.standings_static)
        self.assertIn("NL", self.standings.standings_static)
        self.assertIn("E", self.standings.standings_static["AL"])
        self.assertIn("NL", self.standings.standings_sim)

    def test_update_standings(self):
        # Mock game object
        game = {
            "home_team": "BAL",
            "away_team": "SFN",
            "home_batting_order": [],
            "away_batting_order": [],
            "home_sp": "person",
            "away_sp": "person1",
            "true_home_score": 5,
            "true_away_score": 4,
            "date": "2019/05/23",
        }
        game = BaseballGame(game, to_sim=False)
        self.standings.update_standings(game, sim=False)
        self.assertEqual(self.standings.standings_static["AL"]["E"]["BAL"]["wins"], 1)
        self.assertEqual(self.standings.standings_static["NL"]["W"]["SFN"]["losses"], 1)

        self.standings.update_standings(game, sim=True)
        self.assertEqual(self.standings.standings_sim["AL"]["E"]["BAL"]["wins"], 1)
        self.assertEqual(self.standings.standings_sim["NL"]["W"]["SFN"]["losses"], 1)
        self.assertNotIn("BAL", self.standings.standings_sim["NL"]["W"])
        self.assertNotIn("SFN", self.standings.standings_sim["AL"]["E"])

    def test_combine_standings(self):
        # This test requires the standings to be updated first
        game1 = {
            "home_team": "BAL",
            "away_team": "TBA",
            "home_batting_order": [],
            "away_batting_order": [],
            "home_sp": "person",
            "away_sp": "person1",
            "true_home_score": 5,
            "true_away_score": 4,
            "date": "2019/05/23",
        }
        game2 = {
            "home_team": "ATL",
            "away_team": "TBA",
            "home_batting_order": [],
            "away_batting_order": [],
            "home_sp": "person",
            "away_sp": "person1",
            "true_home_score": 5,
            "true_away_score": 4,
            "date": "2019/05/24",
        }
        game1 = BaseballGame(game1, to_sim=False)
        game2 = BaseballGame(game2, to_sim=False)
        self.standings.update_standings(game1, sim=False)
        self.standings.update_standings(game2, sim=True)
        combined_standings = self.standings.combine_standings()
        # Make sure there are no extra keys added
        self.assertEqual(set(combined_standings.keys()), set(["NL", "AL"]))
        self.assertEqual(set(combined_standings["NL"].keys()), set(["E", "W", "C"]))
        self.assertEqual(set(combined_standings["AL"].keys()), set(["E", "W", "C"]))
        self.assertEqual(combined_standings["NL"]["E"]["ATL"]["wins"], 1)
        self.assertEqual(combined_standings["NL"]["E"]["ATL"]["losses"], 0)
        self.assertEqual(combined_standings["AL"]["E"]["BAL"]["wins"], 1)
        self.assertEqual(combined_standings["AL"]["E"]["BAL"]["losses"], 0)
        self.assertEqual(combined_standings["AL"]["E"]["TBA"]["wins"], 0)
        self.assertEqual(combined_standings["AL"]["E"]["TBA"]["losses"], 2)

    #  Test to make sure that
    # def test_calculate_seeds(self):
    #     # This test requires more comprehensive data and updates
    #     seeds = self.standings.calculate_seeds()
    #     # Assertions based on the expected seeds

    # def test_reset(self):
    #     self.standings.reset()
    #     self.assertEqual(len(self.standings.standings_sim["AL"]["E"]), 0)
    #     self.assertEqual(len(self.standings.standings_static["AL"]["E"]), 0)
    #     # More assertions based on the expected state after reset


class TestSchedule(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Mock data for MLBTeams
        all_games_path = "/home/projects/baseball-MCS/data/intermediate/all_games.json"
        data_stop_date = "2023/03/15"
        simulator = EloSimulator()

        self.schedule = Schedule(all_games_path, data_stop_date, simulator)

    def test_data_types(self):
        for season in self.schedule.seasons:
            for game in season.reg_season_complete:
                self.assertIsInstance(game, BaseballGame)

            for game in season.reg_season_to_sim:
                self.assertIsInstance(game, BaseballGame)

    def test_sim(self):
        n = 1
        analyzer = Analyzer(n=n)
        analyzer = self.schedule.sim(analyzer, n=n)
        for game in self.schedule.seasons[-1].reg_season_to_sim:
            self.assertTrue(game.done)

    def test_num_games(self):
        self.assertGreaterEqual(len(self.schedule.seasons[-1]), 2420)
        n = 1
        analyzer = Analyzer(n=n)
        analyzer = self.schedule.sim(analyzer, n=n)
        combined_standings = self.schedule.seasons[-1].standings.combine_standings()
        for league in ["AL", "NL"]:
            for division in ["E", "W", "C"]:
                self.assertEqual(len(combined_standings[league][division]), 5)
                for team, wl in combined_standings[league][division].items():
                    self.assertGreaterEqual(wl["losses"] + wl["wins"], 160)


class TestElo(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.simulator = EloSimulator(home_advantage=0)

    def test_inital(self):
        game = {
            "home_team": "BAL",
            "away_team": "SFN",
            "home_batting_order": [],
            "away_batting_order": [],
            "home_sp": "person",
            "away_sp": "person1",
            "true_home_score": 5,
            "true_away_score": 4,
            "date": "2019/05/23",
        }
        game = BaseballGame(game=game)
        self.simulator.train(game)
        self.assertEqual(self.simulator.get_elo("BAL"), [1500, 1510])
        self.assertEqual(self.simulator.get_elo("SFN"), [1500, 1490])

    def test_zero_sum(self):
        self.simulator.home_advantage = 100
        game = {
            "home_team": "BAL",
            "away_team": "SFN",
            "home_batting_order": [],
            "away_batting_order": [],
            "home_sp": "person",
            "away_sp": "person1",
            "true_home_score": 5,
            "true_away_score": 4,
            "date": "2019/05/23",
        }
        game = BaseballGame(game=game)
        self.simulator.train(game)
        self.assertEqual(
            self.simulator.get_elo("BAL")[-1] + self.simulator.get_elo("SFN")[-1], 3000
        )


if __name__ == "__main__":
    unittest.main()
