from pprint import pprint
from collections import Counter
import json


def parse_id(game, lst):
    game["home_team"] = lst[1][:3]
    game["date"] = lst[1][3:]


def parse_info(game, lst):
    game[lst[1]] = lst[2]


def parse_start_sub(game, lst):
    lst[5] = int(lst[5])
    lst[3] = int(lst[3])
    if lst[5] == 1:
        if lst[3] == 0:
            game["cur_pitcher_visit"] = lst[1]
        if lst[3] == 1:
            game["cur_pitcher_home"] = lst[1]
        if lst[0] == "start":
            if lst[3] == 0:
                game["visit_sp"] = lst[1]
            if lst[3] == 1:
                game["home_sp"] = lst[1]


# Takes in path to EVX file and returns list of dicts. Each element in list is a game. Keys
# and values are parsed based on functions above. plays are stored as a list of each play.
def parse_EVX(path):
    all_games = []
    first = 1
    with open(path) as f:
        for line in f:
            line = line.strip("\n")
            line = line.split(",")

            match line[0]:
                case "id":
                    if not first:
                        del cur_game["cur_pitcher_vist"]
                        del cur_game["cur_pitcher_home"]
                        all_games.append(cur_game)
                    first = 0
                    cur_game = {"plays": []}
                    parse_id(cur_game, line)
                case "info":
                    parse_info(cur_game, line)
                case "start":
                    parse_start_sub(cur_game, line)
                case "sub":
                    parse_start_sub(cur_game, line)
                case "play":
                    parse_play(cur_game, line)
    return all_games


# Extended parse_outcome function
def parse_outcome(outcome_code):
    outcome_mapping = {
        "K": "strikeout",
        "S": "single",
        "D": "double",
        "T": "triple",
        "H": "homerun",
        "W": "walk",
        "GO": "groundout",
        "FO": "flyout",
        "HP": "walk",  # Hit by Pitch, categorized as a walk
        "/G": "groundout",
        "/F": "flyout",
        "/L": "lineout",
        "/P": "popout",
    }

    for code, full_word in outcome_mapping.items():
        if code in outcome_code:
            return full_word

    return "unknown"  # Default if the code is not recognized


# Updated parse_play function
def parse_play(game, lst):
    lst[2] = int(lst[2])
    lst[1] = int(lst[1])
    cur_pitcher = game["cur_pitcher_home"] if lst[2] == 1 else game["cur_pitcher_visit"]
    num_pitches = -99 if lst[5] == "" else len(lst[5])
    outcome = parse_outcome(lst[6])
    play = {
        "inning": lst[1],
        "pitcher": cur_pitcher,
        "batter": lst[3],
        "num_pitches": num_pitches,
        "outcome": outcome,
        "raw_outcome": lst[6],
    }
    if "plays" not in game:
        game["plays"] = []
    game["plays"].append(play)


# Enhanced function to count the frequency of each outcome type across all games
# and provide additional statistics and sanity checks
def analyze_outcomes(games):
    outcome_counter = Counter()
    total_plays = 0
    total_games = len(games)

    # Counting outcomes and total plays
    for game in games:
        for play in game.get("plays", []):
            outcome_counter[play["outcome"]] += 1
            total_plays += 1

    # Calculating outcome probabilities
    outcome_probabilities = {
        outcome: count / total_plays for outcome, count in outcome_counter.items()
    }

    # Sanity Checks
    sanity_checks = {
        "prob_sum": round(sum(outcome_probabilities.values()), 2) == 1.0,
        "missing_home_team_or_date": any(
            "home_team" not in game or "date" not in game for game in games
        ),
        "games_with_no_plays": sum(1 for game in games if not game.get("plays")),
    }

    # Summary Stats
    summary_stats = {
        "total_games": total_games,
        "total_plays": total_plays,
    }

    # Combine all stats into one dictionary for easier output
    all_stats = {
        "Outcome Counts": outcome_counter,
        "Outcome Probabilities": outcome_probabilities,
        "Summary Stats": summary_stats,
        "Sanity Checks": sanity_checks,
    }

    pprint(all_stats)


def identify_unknown_codes(games):
    unknown_codes = Counter()

    for game in games:
        for play in game.get("plays", []):
            if play["outcome"] == "unknown":
                # Assuming the original outcome code is stored in a 'raw_outcome' field in the play dictionary
                # If it's stored differently, this line should be adjusted
                unknown_codes[
                    play.get("raw_outcome", "N/A")
                ] += 1  # 'N/A' indicates that the raw outcome is missing

    return unknown_codes


import os
import json


def aggregate_EVX_files(root_directory):
    all_games = []
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith(".EVA") or file.endswith(".EVN"):
                file_path = os.path.join(root, file)
                games = parse_EVX(file_path)
                all_games.extend(games)
    return all_games


import pandas as pd


def EVX_json_to_csv(path):
    with open(path, "r") as f:
        all_games = json.load(f)

    rows = []
    for game in all_games:
        for play in game.get("plays", []):
            rows.append(
                {
                    "pitcher": play["pitcher"],
                    "batter": play["batter"],
                    "outcome": play["outcome"],
                }
            )
    df = pd.DataFrame(rows)
    df.to_csv("plays.csv")


if __name__ == "__main__":
    # root_directory = "../data/playbyplay"  # Replace with your actual root directory
    # all_games = aggregate_EVX_files(root_directory)
    # analyze_outcomes(all_games)

    # # Save the object as a JSON file
    # with open('all_games.json', 'w') as f:
    #     json.dump(all_games, f)
    # EVX_json_to_csv('./all_games.json')
    f = open("../../data/intermediate/all_games.json")
    games = json.load(f)
    print(games[0].keys())
    print(games[0]["home_team"])
