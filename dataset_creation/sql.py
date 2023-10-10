import sqlite3
from parsers import parse_EVX
from pprint import pprint

con = sqlite3.connect(':memory:')
cur = con.cursor()

cur.execute('''CREATE TABLE players
               (player_id,team_id, position, start_date, end_date, last_game_played)''')

evx = parse_EVX('../data/playbyplay/2011eve/2011ANA.EVA')
pprint(evx[0])






