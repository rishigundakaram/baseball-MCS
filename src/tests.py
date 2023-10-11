import unittest
import random
from copy import deepcopy
from game import BaseballGame
from parsers import parse_schedule_file

class TestBaseballGame(unittest.TestCase):
    def setUp(self):
        self.transition_probs = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.3]  # sample probabilities
        self.home_team = ["Player1", "Player2", "Player3"]  # sample home team
        self.away_team = ["Player4", "Player5", "Player6"]  # sample away team

    def test_switching_teams(self):
        # Game 1
        # game1 = BaseballGame(self.transition_probs, self.away_team, self.home_team)
        random.seed(1)
        game1 = BaseballGame(self.transition_probs, self.home_team, self.away_team)
        game1.play()

        # Game 2
        random.seed(1)  # resetting the seed

        game2 = BaseballGame(self.transition_probs, self.away_team, self.home_team)
        game2.play()

        # Test if switching home and away teams has no effect on the outcome
        self.assertEqual(game1.home_score, game2.home_score)
        self.assertEqual(game1.away_score, game2.away_score)

class TestSchedule(unittest.TestCase):
    def test_equal_games(self):
        # Parse the schedule file
        df = parse_schedule_file('./data/schedule_2023.txt')

        # Count the games played by each team
        home_games = df['Home'].value_counts()
        away_games = df['Away'].value_counts()
        total_games = home_games.add(away_games, fill_value=0)

        # Get the number of games played by the first team
        first_team_games = total_games[0]

        # Check that each team plays the same number of games
        for team, games in total_games.items():
            self.assertEqual(games, first_team_games, f'Team {team} played a different number of games.')

if __name__ == '__main__':
    unittest.main()
