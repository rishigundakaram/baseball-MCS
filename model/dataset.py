import sqlite3
import os
import pandas as pd

"""
Here we are going to explain the components and logic of the master dataset: 
TABLES: 

1. schedule: [GameID, date, hometeam, awayteam, winner] (up to 2022)
2. lineup: a dataframe of [gameID, team, date, batting order, starting pitcher, relievers used] (2001-2019)
3. batters: a dataframe of [batter_id, season, stats...] (up to 2021)
4. pitchers: a dataframe of [pitcher_id, season, stats...] (up to 2021)
5. plays: a dataframe of [gameID, pitcher_id, batter_id, num_outs, outcome] 
6. transition stats: a dataframe of [date, current state, outcome, next state]

dates are stored as 'yyyy-mm-dd'
need to add date to at bat and transition stats
need to add season start and end dates
"""

class master_dataset: 
    """
    This is the class for all of the possible data that a model can access while training.
    """
    def __init__(self, db_path) -> None:
        self.connection = sqlite3.connect(db_path)
        pass
    
    def get_batting_order(self,team, date): 
        """
        return the most likely batting order for a team on a given date
        """
    
    def get_pitcher_stats(self,pitcher_id, date): 
        """
        return the pitcher stats from the previous season
        """
        season = self.get_prev_season(date)
        q = f"""SELECT * FROM pitchers WHERE season <=
        '{season}' and playerID == '{pitcher_id}' ORDER BY season DESC LIMIT 1"""
        return pd.read_sql_query(q, self.connection)

    def get_batter_stats(self,batter_id, date): 
        """
        return the batter stats from previous season
        """
        season = self.get_prev_season(date)
        q = f"""SELECT * FROM batters WHERE season <=
        '{season}' and playerID == '{batter_id}' ORDER BY season DESC LIMIT 1"""
        return pd.read_sql_query(q, self.connection)


    def get_last_pitchers(self,team_id, date, n): 
        """
        return the last n starting pitchers and last n relievers used in previous games and the dates of their games.
        """
        q = f"""SELECT date,p1ID,p1PC,p2ID,p2PC,p3ID,p3PC,p4ID,p4PC,p5ID,p5PC,p6ID,p6PC,p7ID,p7PC,p8ID,
p8PC,p9ID,p9PC,p10ID,p10PC,p11ID,p11PC,p12ID,p12PC,p13ID,p13PC FROM lineup WHERE date < 
'{date}'  and team == '{team_id}' ORDER BY date DESC LIMIT {n}"""
        return pd.read_sql_query(q, self.connection)


    def get_prev_season(self,date): 
        """
        return the previous season as an int given date in format: yyyy-mm-dd
        """
        cur = self.connection.cursor()
        cur.execute(f"SELECT season FROM schedule WHERE date > '{date}' ORDER BY season ASC LIMIT 1")
        rows = cur.fetchall()
        season_after = int(rows[0][0])

        cur.execute(f"SELECT season FROM schedule WHERE date < '{date}' ORDER BY season DESC LIMIT 1")
        rows = cur.fetchall()
        season_before = int(rows[0][0])
        if season_after == season_before: 
            return season_after - 1
        return season_before
    
    def get_transitions(self, start_date, end_date): 
        q = f"SELECT * FROM transitions WHERE date > '{start_date}' AND date < '{end_date}'"
        return pd.read_sql_query(q, self.connection)
    
    def get_plays(self, start_date, end_date): 
        q = f"SELECT * FROM plays WHERE date > '{start_date}' AND date < '{end_date}'"
        return pd.read_sql_query(q, self.connection)
    
    def get_schedule(self, start_date, end_date): 
        q = f"SELECT * FROM schedule WHERE date > '{start_date}' AND date < '{end_date}'"
        return pd.read_sql_query(q, self.connection)
    
    def get_lineup(self, start_date, end_date): 
        q = f"SELECT * FROM lineup WHERE date > '{start_date}' AND date < '{end_date}'"
        return pd.read_sql_query(q, self.connection)

def insert_lineup(con, data):
    columns = [
        'p1ID', 'p1PC', 'p2ID', 'p2PC',
        'p3ID', 'p3PC', 'p4ID', 'p4PC',
        'p5ID', 'p5PC', 'p6ID', 'p6PC',
        'p7ID', 'p7PC', 'p8ID', 'p8PC',
        'p9ID', 'p9PC', 'p10ID', 'p10PC',
        'p11ID', 'p11PC', 'p12ID', 'p12PC',
        'p13ID', 'p13PC', 
    ]
    for col in columns: 
        if col not in data: 
            if 'PC' in col: 
                data[col] = 0
            else: 
                data[col] = 'NULL'
    con.execute(
    f'''INSERT INTO lineup VALUES ('{data['gameID']}', '{data['date']}', '{data['team']}',
                '{data['bo1ID']}', '{data['bo2ID']}',
                '{data['bo3ID']}', '{data['bo4ID']}',
                '{data['bo5ID']}', '{data['bo6ID']}',
                '{data['bo7ID']}', '{data['bo8ID']}',
                '{data['bo9ID']}',
                '{data['p1ID']}', {data['p1PC']}, 
                '{data['p2ID']}', {data['p2PC']},
                '{data['p3ID']}', {data['p3PC']}, 
                '{data['p4ID']}', {data['p4PC']}, 
                '{data['p5ID']}', {data['p5PC']}, 
                '{data['p6ID']}', {data['p6PC']},
                '{data['p7ID']}', {data['p7PC']}, 
                '{data['p8ID']}', {data['p8PC']}, 
                '{data['p9ID']}', {data['p9PC']}, 
                '{data['p10ID']}', {data['p10PC']},
                '{data['p11ID']}', {data['p11PC']}, 
                '{data['p12ID']}', {data['p12PC']}, 
                '{data['p13ID']}', {data['p13PC']}
    );''')
    
def parse_evx(path, con): 
    first = 1
    with open(path, 'r') as f: 
        for idx, line in enumerate(f):
            line = line.strip('\n')
            line = line.split(',')
            if len(line) == 0: 
                    break
            match line[0]:
                case 'id': 
                    if not first: 
                        insert_lineup(con, home_data)
                        insert_lineup(con, away_data)
                    first = 0
                    home_data = {}
                    away_data = {}
                    h_num_pitchers = 1
                    h_pc = 0
                    a_num_pitchers = 1
                    a_pc = 0
                    home_data['gameID'] = line[1]
                    away_data['gameID'] = line[1]
                case 'info': 
                    if line[1] == 'visteam': 
                        away_data['team'] = line[2]
                    elif line[1] == 'hometeam': 
                        home_data['team'] = line[2]
                    elif line[1] == 'date': 
                        home_data['date'] = line[2][:4] + '-' + line[2][5:7] + '-' + line[2][8:]
                        away_data['date'] = line[2][:4] + '-' + line[2][5:7] + '-' + line[2][8:]
                case 'start': 
                    if line[3] == '0': 
                        data = away_data
                    else: 
                        data = home_data
                    bo = int(line[4])

                    id = line[1]
                    fp = line[-1]
                    if fp == '1': 
                        data['p1ID'] = id
                        data['p1PC'] = 0
                    if bo != '0': 
                        data[f'bo{bo}ID'] = id
                case 'sub':
                    fp = line[-1]
                    id = line[1]
                    if fp == '1':
                        if line[3] == '0': 
                            data = away_data
                            a_num_pitchers += 1
                            r = a_num_pitchers
                        else: 
                            data = home_data
                            h_num_pitchers += 1
                            r = h_num_pitchers
                        data[f'p{r}ID'] = id
                        data[f'p{r}PC'] = 0
                    
                case 'play': 
                    if line[2] == '0': 
                        data = home_data
                        r = h_num_pitchers
                    else: 
                        data = away_data
                        r = a_num_pitchers
                    pc = int(line[4][0]) + int(line[4][1])
                    data[f'p{r}PC'] += pc



def add_outcome(x): 
    if "G" in x: 
        return "groundout"
    elif "F" in x: 
        return "flyout"
    elif "K" in x: 
        return "strikeout"
    elif "S" in x: 
        return "single"
    elif "D" in x: 
        return "double"
    elif "T" in x: 
        return "triple"
    elif "W" in x or "HP" in x: 
        return "walk"
    elif "H" in x: 
        return "homerun"
    else: 
        return "other"

def schedule_table(cursor, game_log_dir, latest_schedule_path): 
    cursor.execute('''CREATE TABLE schedule (gameID text, date DATE, season text, hometeam text, awayteam text, winner int)''')
    logs = os.listdir(game_log_dir)
    for file in logs: 
        if file[0] == '.': 
            continue
        season = file[2:6]
        with open(os.path.join(game_log_dir, file), 'r') as f: 
            for line in f: 
                line = line.split(',')
                date = line[0].strip('\"')
                date = date[:4] + '-' + date[4:6] + '-' + date[6:]
                game_id = line[6].strip('\"') + line[0].strip('\"') + line[1].strip('\"')
                hometeam = line[6].strip('\"')
                awayteam = line[3].strip('\"')
                home_score = int(line[10])
                away_score = int(line[9])
                winner = home_score - away_score
                cursor.execute(f"INSERT INTO schedule VALUES ('{game_id}','{date}','{season}', '{hometeam}','{awayteam}',{winner})")
    with open(latest_schedule_path) as file: 
        for line in file: 
            line = line.split(',')
            date = line[0].strip('\"')
            date = date[:4] + '-' + date[4:6] + '-' + date[6:]
            game_id = line[6].strip('\"') + line[0].strip('\"') + line[1].strip('\"')
            hometeam = line[6].strip('\"')
            awayteam = line[3].strip('\"')
            cursor.execute(f"INSERT INTO schedule VALUES ('{game_id}','{date}','{season}', '{hometeam}','{awayteam}',NULL)")


def roster_table(cursor, play_by_play_dir): 
    cursor.execute(
    '''CREATE TABLE lineup (gameID text, 
                date DATE, team text, 
                bo1ID text, bo2ID text,
                bo3ID text, bo4ID text,
                bo5ID text, bo6ID text,
                bo7ID text, bo8ID text,
                bo9ID text,
                p1Id text, p1PC int, 
                p2ID text, p2PC int,  
                p3ID text, p3PC int, 
                p4ID text, p4PC int,
                p5ID text, p5PC int,
                p6ID text, p6PC int,
                p7ID text, p7PC int,
                p8ID text, p8PC int,
                p9ID text, p9PC int,
                p10ID text, p10PC int,
                p11ID text, p11PC int, 
                p12ID text, p12PC int, 
                p13ID text, p13PC int )
    ''')
    for direc in os.listdir(play_by_play_dir): 
        for evx in os.listdir(play_by_play_dir + direc): 
            parse_evx(play_by_play_dir + direc + '/' + evx, con=cursor)

def map_ids(people_path):
    people_map = {}
    with open(people_path) as f: 
        for line in f: 
            line = line[:-1]
            line = line.split(',')
            if line[0] == 'playerID':
                continue
            people_map[line[0]] = line[-2]
    return people_map

def map_game_ids(game_info_path): 
    game_map = {}
    with open(game_info_path) as f: 
        for line in f: 
            line = line[:-1]
            line = line.split(',')
            if line[1] == 'date':
                comp = line[2].split('/')
                year = '20' + comp[2]
                month = comp[0] if len(comp[0]) == 2 else '0' + comp[1]
                day = comp[2]
                game_map[line[0]] = year + '-' + month + '-' + day
    return game_map
    
def batting_pitching_table(connection, lahman_path, people_path, batting=True): 
    df = pd.read_csv(lahman_path)
    df = df.drop(columns=['lgID'])

    lahman_to_retrosheet = map_ids(people_path)
    df['playerID'] = df['playerID'].apply(lambda x: lahman_to_retrosheet[x])
    sub_df = df.groupby(['playerID', 'yearID']).sum().reset_index()
    sub_df = sub_df.drop(columns=['stint'])
    sub_df = sub_df.rename(columns={'yearID': "season"})
    if batting: 
        sub_df.to_sql('batters', con=connection, index=False)
    else: 
        sub_df.to_sql('pitchers', con=connection, index=False)

def plays_table(connection, plays_path): 
    plays_data = pd.read_csv(plays_path)
    plays_data["outcome"] = plays_data["play_str"].apply(add_outcome)
    plays_data["cur_outs"] =  plays_data["out"] - plays_data["play_outs"]
    data = plays_data[["game_id", "pitcher", "player_id", "outcome", "cur_outs"]]
    data.to_sql('plays', con=connection, index=False)

def transitions_table(connection, plays_path, game_info_path): 
    plays_data = pd.read_csv(plays_path)
    game_map = map_game_ids(game_info_path)
    plays_data["outcome"] = plays_data["play_str"].apply(add_outcome)
    
    states = [
        [0,0,0,0],[1,0,0,0],[0,1,0,0],[0,0,1,0],[1,1,0,0],[1,0,1,0],[0,1,1,0],[1,1,1,0],
        [0,0,0,1],[1,0,0,1],[0,1,0,1],[0,0,1,1],[1,1,0,1],[1,0,1,1],[0,1,1,1],[1,1,1,1],
        [0,0,0,2],[1,0,0,2],[0,1,0,2],[0,0,1,2],[1,1,0,2],[1,0,1,2],[0,1,1,2],[1,1,1,2],
        [0,0,0,3]
    ]
    transitions = pd.DataFrame([], columns=['game_id', 'pre_1', 'pre_2', 'pre_3', 'pre_outs', 'post_1','post_2', 'post_3', 'post_outs', 'runs', 'outcome'])
    
    transitions['pre_1'] = (plays_data['pre_state'].apply(lambda x: states[x-1][0]))
    transitions['pre_2'] = (plays_data['pre_state'].apply(lambda x: states[x-1][1]))
    transitions['pre_3'] = (plays_data['pre_state'].apply(lambda x: states[x-1][2]))
    transitions['pre_outs'] = (plays_data['pre_state'].apply(lambda x: states[x-1][3]))
    transitions['post_1'] = (plays_data['post_state'].apply(lambda x: states[min(x-1, 24)][0]))
    transitions['post_2'] = (plays_data['post_state'].apply(lambda x: states[min(x-1, 24)][1]))
    transitions['post_3'] = (plays_data['post_state'].apply(lambda x: states[min(x-1, 24)][2]))
    transitions['post_outs'] = (plays_data['post_state'].apply(lambda x: states[min(x-1, 24)][3]))
    transitions['runs'] = plays_data['play_runs']
    transitions['outcome'] = plays_data['outcome']
    transitions['game_id'] = plays_data['game_id']
    transitions['date'] = plays_data['game_id'].apply(lambda x: game_map[x])
    transitions.to_sql('transitions', con=connection, index=False)

if __name__ == '__main__': 
    
    game_log_dir = '../data/game_logs/'
    play_by_play_dir = '../data/playbyplay/'
    lahman_batting_path = '../data/lahman/core/Batting.csv'
    lahman_pitching_path = '../data/lahman/core/Pitching.csv'
    people_path = '../data/lahman/core/People.csv'
    plays_path = '../retrosheet_parsing/data/plays.csv'
    game_info_path = '../retrosheet_parsing/data/info.csv'
    schedule_path = '../data/schedule/2022SKED.TXT'
    db_path = "baseball.db"
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    schedule_table(cursor, game_log_dir, schedule_path)
    roster_table(cursor, play_by_play_dir)
    batting_pitching_table(connection, lahman_batting_path, people_path, batting=True)
    batting_pitching_table(connection, lahman_pitching_path, people_path, batting=False)
    plays_table(connection, plays_path)
    transitions_table(connection, plays_path, game_info_path)

    connection.commit()
    connection.close()