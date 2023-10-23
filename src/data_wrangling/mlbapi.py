import statsapi

mlb_team_mapping = {
    110: "BAL",
    111: "BOS",
    147: "NYY",
    139: "TBR",
    141: "TOR",
    145: "CWS",
    114: "CLE",
    116: "DET",
    118: "KCR",
    142: "MIN",
    117: "HOU",
    108: "LAA",
    133: "OAK",
    136: "SEA",
    140: "TEX",
    144: "ATL",
    146: "MIA",
    121: "NYM",
    143: "PHI",
    120: "WSN",
    112: "CHC",
    113: "CIN",
    158: "MIL",
    134: "PIT",
    138: "STL",
    109: "ARI",
    115: "COL",
    119: "LAD",
    135: "SD",
    137: "SF",
}


def fetch_mlb_play_by_play(start_date, end_date, TeamIDmap, PlayerIDmap):
    # Get the list of games on the specified date
    schedule = statsapi.schedule(start_date=start_date, end_date=end_date, sportId=1)

    # Initialize an empty dictionary to store play-by-play data
    all_games_play_by_play = {}

    # Loop through each game to fetch the play-by-play data
    games = []
    for game in schedule:
        cur_game = {}

        # cur_game["game_id"] = game["game_id"]
        cur_game["away_team"] = TeamIDmap[game["away_id"]]
        cur_game["home_team"] = TeamIDmap[game["home_id"]]

        cur_game["regular_season"] = True if game["game_type"] == "R" else False
        cur_game["is_done"] = True if game["status"] == "Final" else False
        cur_game["home_score"] = game["home_score"]
        cur_game["away_score"] = game["away_score"]
        cur_game["plays"] = []

        # assemble retrosheet id
        game_date = game["game_date"]
        game_num = str(game["game_num"] - 1)
        year = str(game_date[:4])
        month = str(game_date[5:7])
        day = str(game_date[8:10])
        cur_game["game_id"] = cur_game["home_team"] + year + month + day + game_num
        cur_game["game_date"] = f"{year}/{month}/{day}"
        game_id = game["game_id"]
        # get the batting orders and starting pitchers for the game
        game_info = statsapi.get("game", {"gamePk": 748549})
        cur_game["home_sp"] = PlayerIDmap[
            game_info["gameData"]["probablePitchers"]["home"]["id"]
        ]
        cur_game["away_sp"] = PlayerIDmap[
            game_info["gameData"]["probablePitchers"]["away"]["id"]
        ]

        boxscore_data = statsapi.get("game_boxscore", {"gamePk": game_id})
        cur_game["home_batting_order"] = [
            PlayerIDmap[i] for i in boxscore_data["teams"]["home"]["battingOrder"]
        ]
        cur_game["away_batting_order"] = [
            PlayerIDmap[i] for i in boxscore_data["teams"]["away"]["battingOrder"]
        ]

        # get the play by play data for the game
        play_by_play_data = statsapi.get("game_playByPlay", {"gamePk": game_id})
        for play in play_by_play_data["allPlays"]:
            parse_play(play, cur_game, PlayerIDmap)

        # Add the play-by-play data to the dictionary, using the game ID as the key
        games.append(cur_game)

    return games


def parse_play(play, cur_game, PlayerIDmap):
    if play["result"]["type"] != "atBat":
        return
    outcome = simplify_outcome(play["result"]["event"])
    if outcome == "Caught Stealing 2B":
        return
    batter = PlayerIDmap[play["matchup"]["batter"]["id"]]
    pitcher = PlayerIDmap[play["matchup"]["pitcher"]["id"]]
    num_pitches = len(play["pitchIndex"])
    cur_game["plays"].append(
        (
            {
                "batter": batter,
                "pitcher": pitcher,
                "outcome": outcome,
                "num_pitches": num_pitches,
                "raw_outcome": None,
            }
        )
    )


def simplify_outcome(outcome):
    outcome_map = {
        "Walk": "walk",
        "Pop Out": "popout",
        "Strikeout": "strikeout",
        "Single": "single",
        "Flyout": "flyout",
        "Lineout": "lineout",
        "Home Run": "homerun",
        "Groundout": "groundout",
        "Grounded Into DP": "groundout",
        "Intent Walk": "walk",
        "Hit By Pitch": "walk",
        "Sac Fly": "flyout",
        "Forceout": "groundout",
        "Field Error": "single",
        "Double": "double",
        "Double Play": "groundout",
        "Triple": "triple",
        "Fielders Choice": "groundout",
        "Catcher Interference": "walk",
        "Fielders Choice Out": "groundout",
        "Fielders Choice": "groundout",
        "Caught Stealing 2B": "unknown",
        "Sac Bunt": "groundout",
        "Strikeout Double Play": "Strikeout",
        "Bunt Pop Out": "popout",
        "Bunt Groundout": "groundout",
        "Bunt Lineout": "lineout",
        "Pickoff 1B": "unknown",
        "Pickoff Caught Stealing 2B": "unkown",
        "Caught Stealing Home": "unknown",
        "Runner Out": "unknown",
        "Sac Fly Double Play": "flyout",
        "Wild Pitch": "walk",
        "Caught Stealing 3B": "unknown",
        "Pickoff 2B": "unknown",
    }
    if outcome not in outcome_map:
        return "unknown"
    return outcome_map[outcome]


import json
import os
from pprint import pprint

# Example usage
# playerIDpath = "./baseball-MCS/data/intermediate/mlb_to_retro_PlayerID_map.json"
playerIDpath = "../../data/intermediate/mlb_to_retro_PlayerID_map.json"
with open(playerIDpath) as js:
    playerIDmap = json.load(js)
playerIDmap = {int(k): v for k, v in playerIDmap.items()}

# TeamIDpath = "./baseball-MCS/data/intermediate/mlb_to_retro_TeamID_map.json"
TeamIDpath = "../../data/intermediate/mlb_to_retro_TeamID_map.json"
with open(TeamIDpath) as js:
    TeamIDmap = json.load(js)
TeamIDmap = {int(k): v for k, v in TeamIDmap.items()}

start_date = "2023-10-22"
end_date = "2023-10-22"
# Replace with the date you are interested in (format: 'YYYY-MM-DD')
games = fetch_mlb_play_by_play(start_date, end_date, TeamIDmap, playerIDmap)
pprint(games)
# result = statsapi.get("game", {"gamePk": 748549})
# print(result)
