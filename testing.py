from dataset_creation.parser import parse_EVX
from pprint import pprint

path = './data/playbyplay/2019eve/2019ANA.EVA'
games = parse_EVX(path)
pprint(games[0])
