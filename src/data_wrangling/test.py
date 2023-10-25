import json
from pprint import pprint

all_games_path = "../../data/intermediate/all_games.json"

with open(all_games_path, "r") as f:
    all_games = json.load(f)

filtered = filter(lambda x: x["date"] == "2023/03/31", all_games)
for s in filtered:
    pprint(s["game_id"])
