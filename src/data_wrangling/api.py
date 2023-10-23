import statsapi


def fetch_mlb_play_by_play(date):
    # Get the list of games on the specified date
    schedule = statsapi.schedule(start_date=date, end_date=date, sportId=1)

    # Initialize an empty dictionary to store play-by-play data
    all_games_play_by_play = {}

    # Loop through each game to fetch the play-by-play data
    games = []
    for game in schedule:
        cur_game = {}
        cur_game["game_id"] = game["game_id"]
        cur_game["away_team"] = game["away_id"]
        cur_game["home_team"] = game["home_id"]
        cur_game["game_date"] = game["game_date"]
        cur_game["regular_season"] = True if game["game_type"] == "R" else False
        cur_game["is_done"] = True if game["status"] == "Final" else False
        cur_game["home_score"] = game["home_score"]
        cur_game["away_score"] = game["away_score"]
        cur_game["plays"] = []

        game_id = game["game_id"]
        # get the batting orders and starting pitchers for the game
        game_info = statsapi.get("game", {"gamePk": 748549})
        cur_game["home_sp"] = game_info["gameData"]["probablePitchers"]["home"]["id"]
        cur_game["away_sp"] = game_info["gameData"]["probablePitchers"]["away"]["id"]

        boxscore_data = statsapi.get("game_boxscore", {"gamePk": game_id})
        cur_game["home_batting_order"] = boxscore_data["teams"]["home"]["battingOrder"]
        cur_game["away_batting_order"] = boxscore_data["teams"]["away"]["battingOrder"]

        # get the play by play data for the game
        play_by_play_data = statsapi.get("game_playByPlay", {"gamePk": game_id})
        for play in play_by_play_data["allPlays"]:
            parse_play(play, cur_game)

        # Add the play-by-play data to the dictionary, using the game ID as the key
        games.append(cur_game)

    return games


def parse_play(play, cur_game):
    if play["result"]["type"] != "atBat":
        return
    outcome = play["result"]["event"]
    batter = play["matchup"]["batter"]["id"]
    pitcher = play["matchup"]["pitcher"]["id"]
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


# Example usage
date = "2023-10-22"
# Replace with the date you are interested in (format: 'YYYY-MM-DD')
games = fetch_mlb_play_by_play(date)
from pprint import pprint

pprint(games)
# result = statsapi.get("game", {"gamePk": 748549})
# print(result)
