import json
from pprint import pprint
import unittest

all_games_path = "../../data/intermediate/all_games.json"

with open(all_games_path, "r") as f:
    all_games = json.load(f)


def duplicates(all_games):
    game_keys = set()
    for game in all_games:
        if game["game_id"] not in game_keys:
            game_keys.add(game["game_id"])
        else:
            pprint(all_games)
            raise Exception
    print("no duplicates")


def import_quality(all_games):
    game_keys = [
        "home_team",
        "away_team",
        "date",
        "home_batting_order",
        "away_batting_order",
        "home_sp",
        "away_sp",
        "home_score",
        "away_score",
        "regular_season",
    ]
    for game in all_games:
        for key in game_keys:
            if key not in game.keys():
                pprint(game)
                raise Exception
    print("passed import quality")


class TestDataStructure(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # This is called once before all tests in this class
        all_games_path = "../../data/intermediate/all_games.json"
        with open(all_games_path, "r") as f:
            self.all_games = json.load(f)

        mlb_to_retro_TeamID_map_path = (
            "../../data/intermediate/mlb_to_retro_TeamID_map.json"
        )
        with open(mlb_to_retro_TeamID_map_path, "r") as f:
            self.team_map = json.load(f)

    def test_duplicates(self):
        game_keys = set()
        for game in all_games:
            if game["game_id"] not in game_keys:
                game_keys.add(game["game_id"])
            else:
                pprint(all_games)
                raise Exception

    def test_import_quality(self):
        game_keys = set(
            [
                "home_team",
                "away_team",
                "date",
                "home_batting_order",
                "away_batting_order",
                "home_sp",
                "away_sp",
                "home_score",
                "away_score",
                "regular_season",
                "plays",
                "is_done",
                "game_id",
            ]
        )
        for game in all_games:
            a = set(game.keys())
            assert (
                game_keys == a
            ), f"actual differences {game_keys - a}, {a - game_keys}, actual game {pprint(game)}"

    def test_team_names(self):
        team_names = set(self.team_map.values())
        for game in self.all_games:
            assert (
                game["home_team"] in team_names and game["away_team"] in team_names
            ), f'gameID: {game["game_id"]}, teams: {game["home_team"], game["away_team"]}'


if __name__ == "__main__":
    unittest.main()
