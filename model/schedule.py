from importlib.machinery import WindowsRegistryFinder
import dataset
from copy import deepcopy
import numpy as np
import random
import pandas as pd

class Game:
    def __init__(self, gameID, date, home, away) -> None:
        self.gameID = gameID
        self.date = date
        self.home = home
        self.away = away
        self.game_number = int(gameID[-1])
        self.completed = False

    def dist(self, h_prob_bo, a_prob_bo, h_prob_sp, a_prob_sp, h_prob_r, a_prob_r): 
        self.h_pred_bo = h_prob_bo
        self.a_pred_bo = a_prob_bo
        self.h_pred_sp = h_prob_sp
        self.a_pred_sp = a_prob_sp
        self.h_pred_r = h_prob_r
        self.a_pred_r = a_prob_r
    
    def used(self, h_bo, a_bo, h_sp, a_sp, h_r, a_r): 
        self.h_bo = h_bo
        self.a_bo = a_bo
        self.h_sp = h_sp
        self.a_sp = a_sp
        self.h_r = h_r
        self.a_r = a_r

    def finish(self, winner=1, run_differential=1): 
        self.winner = winner
        self.run_differential = run_differential
        self.completed = True
    
    def parse_used(self, home_stats, away_stats): 
        h_row = list(home_stats.iloc[0])
        a_row = list(away_stats.iloc[0])
        h_bo = h_row[3:12]
        a_bo = a_row[3:12]
        h_sp = h_row[13]
        a_sp = a_row[13]
        h_r = []
        for i in h_row[14:]: 
            if i == 'NULL':
                break
            elif isinstance(i, int):
                continue
            h_r.append(i)
        a_r = []
        for i in h_row[14:]: 
            if i == 'NULL':
                break
            elif isinstance(i, int):
                continue
            a_r.append(i)
        self.used(h_bo, a_bo, h_sp, a_sp, h_r, a_r)

class Schedule: 
    """
    for each game, give the starting pitcher, and an ordered lists of reliever
    give a list of games in order where each game depends on games before it
    """
    def __init__(self, train_start, train_end, test_start, test_end) -> None:
        self.train_games = None
        self.test_games = None
        self.train_start = train_start
        self.train_end = train_end
        self.test_start = test_start
        self.test_end = test_end
     
    def process(self,database, starter_window=180, sp_window=10, bo_window=10, r_window=10): 
        """
        two data structures: 
            df of schedule: df of [date, gameID, hometeam, awayteam, winner]
            dict of last games: {team: [Games sorted by date]}
            dict of train games: {gameID: Game}
            dict of test games: {gameID: Game}
        """
        self.schedule = database.get_schedule(self.train_start, self.test_end)
        sub_df = self.schedule.loc[
            (self.schedule['winner'] != 0) & 
            (self.schedule['winner'] != 1)
        ]
        self.idx_test = sub_df.index[0]
        self.idx_train = starter_window
        self.lineup = database.get_lineup(self.train_start, self.train_end)

        self.starter_core = {}
        self.train_core = {}
        self.test_core = {}

        self.train_games = {}
        self.test_games = {}
        
        for idx, row in self.schedule.iterrows(): 
            gameID = row[0]
            date = row[1]
            home_team = row[3]
            away_team = row[4]
            winner = row[5]
            cur_game = Game(gameID, date, home=home_team, away=away_team)
            if idx < self.idx_train or idx < self.idx_test: 
                home_stats = self.lineup.loc[
                    (self.lineup['gameID'] == gameID) & 
                    (self.lineup['team'] == home_team)
                ]
                away_stats = self.lineup.loc[
                    (self.lineup['gameID'] == gameID) & 
                    (self.lineup['team'] == away_team)
                ]
                cur_game.parse_used(home_stats, away_stats)
                cur_game.finish(winner > 0, winner)
                if  self.idx_train <= idx < self.idx_test: 
                    h_sp = self.sample_sp(home_team, window=sp_window, train=True)
                    a_sp = self.sample_sp(away_team, window=sp_window, train=True)
                    h_bo = self.sample_bo(home_team, window=bo_window, train=True)
                    a_bo = self.sample_bo(away_team, window=bo_window, train=True)
                    h_r = self.sample_r(home_team, window=r_window, train=True)
                    a_r = self.sample_r(away_team, window=r_window, train=True)
                    cur_game.dist(h_sp, a_sp, h_bo, a_bo, h_r, a_r)
                    self.__add_game(self.train_core, home_team, away_team, cur_game)
                    self.train_games[gameID] = cur_game
                else: 
                    self.__add_game(self.starter_core, home_team, away_team, cur_game)
            else: 
                self.test_games[gameID] = cur_game
                self.__add_game(self.test_core, home_stats, away_stats, cur_game)

    def reset(self):
        self.test_core = {}
        self.test_games = {}
        for idx, row in self.schedule.iterrows(): 
            if idx < self.idx_test: 
                continue
            gameID = row[0]
            date = row[1]
            home_team = row[3]
            away_team = row[4]
            winner = row[5]
            cur_game = Game(gameID, date, home=home_team, away=away_team)
            self.test_games[gameID] = cur_game
            self.__add_game(self.test_core, home_team, away_team, cur_game)

    def __add_game(self, core, home_team, away_team, game): 
        if home_team not in core: 
            core[home_team] = [game]
        else: 
            core[home_team].append(game)
        if away_team not in core: 
            core[away_team] = [game]
        else: 
            core[away_team].append(game)
    
    def __get_last_n_games(self, team, train=True, n=5): 
        if train: 
            cur_core = self.train_core
            starter_core = self.starter_core
        else: 
            cur_core = self.test_core
            starter_core = self.train_core
        m = len(cur_core[team])
        if m >= n: 
            return cur_core[team][:-n]
        return starter_core[team][:-(n-m)] + cur_core[team][:-m]

    def sample_sp(self, team, window=10, train=True): 
        # get last n games and put in player who played the latest game who hasn't played n-1 games
        games = self.__get_last_n_games(team, window, train=train)
        home_away = [i.home == team for i in games]
        sps = []
        for idx in range(len(home_away)): 
            if home_away[idx]: 
                sps.append(games[idx].h_sp)
            else: 
                sps.append(games[idx].a_sp)
        track = set()
        last = None
        for sp in sps[-1:]: 
            if sp not in track: 
                track.add(sp)
                last = sp
            elif sp in track: 
                return last
    def sample_bo(self, team, window=10, train=True):
        games = self.__get_last_n_games(team, window, train=train)
        home_away = [i.home == team for i in games]
        bo = []
        for idx in range(len(home_away)): 
            if home_away[idx]: 
                bo.append(games[idx].h_bo)
            else: 
                bo.append(games[idx].a_bo)
        return random.choice(bo)
    
    def sample_r(self, team, window=10, train=True): 
        games = self.__get_last_n_games(team, window, train=train)
        home_away = [i.home == team for i in games]
        relievers = []
        for idx in range(len(home_away)): 
            if home_away[idx]: 
                relievers.append(games[idx].h_r)
            else: 
                relievers.append(games[idx].a_r)
        # get all relievers from last n games, filter out relievers that played in both of last games
        # pick a random ordering of 
        set1 = set(relievers[-1])
        set2 = set(relievers[-2])
        unavailable = set1.intersection(set2)
        available = set()
        for game in relievers: 
            for r in game: 
                if r not in unavailable:
                    available.add(r)
        return random.shuffle(list(available))

    def iter_train(self): 
        for idx, row in self.schedule.iterrows(): 
            if idx < self.idx_train or idx >= self.idx_test: 
                continue
            gameID = row[0]
            yield self.train_games[gameID]
        pass
    
    def iter_test(self): 
        for idx, row in self.schedule.iterrows(): 
            if idx < self.idx_test: 
                continue
            gameID = row[0]
            yield self.train_games[gameID]
        pass
    
    def aggregate(self): 
        data = pd.DataFrame(columns=['gameID', 'home', 'away', 'winner', 'run_differential'])
        for game in self.test_games.values(): 
            data.append({
                'gameID': game.gameID,
                'date': game.date, 
                'home': game.home,
                'away': game.away,
                'winner': game.winner,
                'run_differential': game.run_differential
            })
        return data

if __name__ == "__main__": 
    database_path = "./baseball.db"
    database = dataset.master_dataset(database_path)
    sked = Schedule('2011-04-01', '2020-04-20', '2020-04-21', '2022-07-20')
    sked.process(database)

