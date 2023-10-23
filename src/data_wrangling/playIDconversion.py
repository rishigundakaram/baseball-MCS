import os
import pandas as pd
import json

if __name__ == "__main__":
    data_path = "../../data/raw/register/data"

    dir = os.listdir(data_path)
    dir = [i for i in dir if "people" in i]

    blocks = []
    for name in dir:
        blocks.append(pd.read_csv(os.path.join(data_path, name), low_memory=False))
    players = pd.concat(blocks)

    players = players[["key_mlbam", "key_retro"]]
    players = players.dropna()
    player_mapping = dict(zip(players["key_mlbam"].astype(int), players["key_retro"]))

    # Save the dictionary to a JSON file
    json_file_path = "../../data/intermediate/mlb_to_retro_ID_map.json"
    with open(json_file_path, "w") as f:
        json.dump(player_mapping, f)
