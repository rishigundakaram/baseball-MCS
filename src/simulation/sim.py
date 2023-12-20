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
from random import randint


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
