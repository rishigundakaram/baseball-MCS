from parsers import parse_EVX
from statistics import parse_stats, parse_id_map
from pprint import pprint

pitcher_path = '../data/pitcher_batter/pitcher_stats.csv'
id_map_path = '../data/player_ids/id_map.csv'

id_map = parse_id_map(id_map_path)
headers, batters = parse_stats(pitcher_path, id_map, batter=False)
pprint(batters)
print(headers)
