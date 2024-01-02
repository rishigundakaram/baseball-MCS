from collections import defaultdict
import pandas as pd
import numpy as np
from static import MLBTeams


def default_standings():
    return {"wins": 0, "losses": 0}


class Analyzer:
    def __init__(self, n=1) -> None:
        self.n = n
        self.playoff_count = defaultdict(int)
        self.world_series = defaultdict(int)
        self.division_winners = defaultdict(int)
        self.record = defaultdict(default_standings)
        self.averaged = False

    def update(self, standings, seeds, world_series_winner):
        self.world_series[world_series_winner] += 1
        combined = standings.combine_standings()
        for league in ["AL", "NL"]:
            for seed in range(1, 7):
                self.playoff_count[seeds[league][seed]] += 1
            for division in ["C", "E", "W"]:
                for team in combined[league][division]:
                    self.record[team]["wins"] += combined[league][division][team][
                        "wins"
                    ]
                    self.record[team]["losses"] += combined[league][division][team][
                        "losses"
                    ]

        for league in ["AL", "NL"]:
            for division in combined[league]:
                # Determine the division winner
                division_teams = combined[league][division]
                division_winner = max(
                    division_teams,
                    key=lambda team: (
                        division_teams[team]["wins"],
                        -division_teams[team]["losses"],
                    ),
                )
                self.division_winners[division_winner] += 1

    def average(self):
        if self.averaged:
            return
        self.playoff_count = {
            key: 100 * round(value / self.n, 2)
            for key, value in self.playoff_count.items()
        }
        self.world_series = {
            key: 100 * round(value / self.n, 3)
            for key, value in self.world_series.items()
        }
        self.division_winners = {
            key: 100 * round(value / self.n, 2)
            for key, value in self.division_winners.items()
        }
        self.record = {
            key: {i: round(j / self.n) for i, j in value.items()}
            for key, value in self.record.items()
        }
        self.averaged = True

    def print(self):
        self.average()
        df = pd.DataFrame(
            columns=[
                "Team",
                "Avg Wins",
                "Avg Losses",
                "Make Playoffs %",
                "Win Division %",
                "Win World Series %",
            ]
        )
        i = 0
        for team in MLBTeams:
            if not MLBTeams[team]["active"]:
                continue

            wins = self.record[team]["wins"]
            losses = self.record[team]["losses"]
            if team not in self.playoff_count:
                po_count = 0
            else:
                po_count = self.playoff_count[team]
            if team not in self.division_winners:
                dw_count = 0
            else:
                dw_count = self.division_winners[team]
            if team not in self.world_series:
                ws_count = 0
            else:
                ws_count = self.world_series[team]
            df.loc[i] = [
                team,
                wins,
                losses,
                po_count,
                dw_count,
                ws_count,
            ]
            i += 1
        return df

    def export(self, elo_simulator=None):
        df = self.print()
        for team in MLBTeams:
            MLBTeams[team]["Elo"] = elo_simulator.get_elo(team)
            MLBTeams[team]["Current Elo"] = round(MLBTeams[team]["Elo"][-1])

        team_info_df = pd.DataFrame.from_dict(MLBTeams, orient="index")
        df = df.merge(team_info_df, left_on="Team", right_index=True)

        division_names = {"E": "East", "W": "West", "C": "Central"}
        df["league"] = df["league"] + " " + df["division"].map(division_names)
        df = df[
            [
                "logo",
                "team_name",
                "league",
                "Elo",
                "Current Elo",
                "Avg Wins",
                "Avg Losses",
                "Make Playoffs %",
                "Win Division %",
                "Win World Series %",
            ]
        ]
        df = df.rename(columns={"team_name": "Team", "league": "League"})
        return df


class Metrics:
    def __init__(self) -> None:
        self.running_brier = 0
        self.num_games = 0

    def update(self, game, home_prob, away_prob):
        actual = [0, 0]
        if game.true_home_score > game.true_away_score:
            actual[0] = 1
        else:
            actual[1] = 1
        self.running_brier += self.brier_score([home_prob, away_prob], actual)
        self.num_games += 1

    def get_brier(self):
        return self.running_brier / self.num_games

    def reset(self):
        self.running_brier = 0
        self.num_games = 0

    def brier_score(self, prediction, actual):
        prediction = np.array(prediction)
        actual = np.array(actual)

        return sum((prediction - actual) ** 2)
