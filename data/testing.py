from dataset_creation.parser import parse_EVX
from dataset_creation.statistics import parse_stats
from pprint import pprint

path = './data/pitcher_batter/pitcher_stats.csv'
headers, batters = parse_stats(path, batter=False)
pprint(batters)
print(headers)
