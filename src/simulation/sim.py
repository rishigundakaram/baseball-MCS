"""
Main Simulation File

Purpose: To simulate the remainder of a baseball season starting from a user-specified date.
    User Input
    User should specify the beginning date for the simulation and how many months of prior training data
Data Preparation
    Load the season schedule corresponding to the user-specified date.
    Create training data for the transition model.
Model Training
    Check if a transition model already exists for the specified beginning date and months of prior training data
    If it does, load that model.
    If it doesn't, train a new transition model.
Data Availability and Constraints
    Ensure the program can handle scenarios where future data is not accessible.
    For example, if the simulation starts at the beginning of the season but real-time data is only available up to the current date in the middle of the season, the program should not use data from the middle of the season.
"""

from typing import Any
from game import BaseballGame
from random import randint, random
from collections import defaultdict


class Simulator:
    def __init__(self) -> None:
        pass

    def train(self, game) -> None:
        return None

    def sim(self, game) -> BaseballGame:
        return game


class RandomSimulator(Simulator):
    def sim(self, game):
        game.home_score = randint(0, 10)
        away_score = randint(0, 10)
        while away_score == game.home_score:
            away_score = randint(0, 10)
        game.away_score = away_score
        game.done = True
        return game

    def train(self, game):
        return 0.5, 0.5


class EloSimulator:
    def __init__(self, base_elo=1500, k_factor=20, home_advantage=50):
        """
        Initialize the Elo Simulator.

        :param teams: List of team names.
        :param base_elo: Base Elo rating for all teams.
        """
        self.k_factor = k_factor
        self.home_advantage = home_advantage
        self.elo = defaultdict(lambda: [base_elo])

    def train(self, game):
        """
        Update Elo ratings after a game, considering home team advantage and ensuring zero-sum.

        :param game: Game object with attributes home_team, away_team, home_score, away_score.
        """
        home_team = game.home_team
        away_team = game.away_team
        home_elo = self.elo[home_team][-1]
        away_elo = self.elo[away_team][-1]

        # Adjust for home team advantage
        home_elo_adjusted = home_elo + self.home_advantage

        # Calculate expected win probabilities
        expected_home_win = 1 / (1 + 10 ** ((away_elo - home_elo_adjusted) / 400))
        expected_away_win = 1 - expected_home_win

        # Determine winner and loser based on game score
        if game.home_score > game.away_score:
            winner, loser = home_team, away_team
            elo_change = self.k_factor * (1 - expected_home_win)
        else:
            winner, loser = away_team, home_team
            elo_change = self.k_factor * expected_home_win

        # Update Elo ratings
        self.elo[winner].append(self.elo[winner][-1] + elo_change)
        self.elo[loser].append(self.elo[loser][-1] - elo_change)

        return expected_home_win, expected_away_win

    def sim(self, game) -> BaseballGame:
        """
        Simulate a game between two teams based on their Elo ratings.

        :param team1: Name of the first team.
        :param team2: Name of the second team.
        """
        # Implement your game simulation logic here
        # For simplicity, let's say the team with the higher Elo rating wins
        home_elo = self.elo[game.home_team][-1] + self.home_advantage
        away_elo = self.elo[game.away_team][-1]
        home_win_prob = 1 / (1 + 10 ** ((away_elo - home_elo) / 400))
        if random() < home_win_prob:
            game.home_score = 1
            game.away_score = 0
        else:
            game.away_score = 1
            game.home_score = 0
        return game

    def get_elo(self, team):
        return self.elo[team][-50:]