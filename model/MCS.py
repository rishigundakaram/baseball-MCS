from sched import scheduler
from torch import _fused_moving_avg_obs_fq_helper
from .transitions import *
import random
from .simulator import Simulator
import pandas as pd    

class MCS_game: 
    def __init__(self, game) -> None:
        self.game = game

        self.outs = 0
        self.home_runs = 0
        self.away_runs = 0
        self.inning = 1
        self.top = True
        self.bases = [0, 0, 0]
    
    def sim(self, regressor, manager, simulator): 
        while not self.check_done(): 
            outcome = regressor.predict(self.pitcher, self.batter, self.game_state)
            # 
            self.bases[0], self.bases[1], self.bases[2], outs, runs = simulator.sample(
                outcome=outcome, 
                outs=self.outs,
                first=self.bases[0],
                second=self.bases[1],
                third=self.bases[2],
            )
            self.add_runs(runs)
            self.add_outs(outs)
            manager(self.game)
        self.game.finish(self.home_runs > self.away_runs, self.home_runs - self.away_runs)

    def check_done(self):
        if self.top: 
            return False
        elif self.home_runs == self.away_runs: 
            return False
        elif self.inning < 9: 
            return False
        return True
    
    def add_outs(self, num_outs): 
        self.outs +=  num_outs
        if self.outs >= 3: 
            self.done = self.check_done()
            if self.top:
                self.top = False
            else: 
                self.inning += 1
                self.top = True
            self.outs = 0
            self.bases = [0,0,0]
    
    def add_runs(self, runs): 
        if self.top == True: 
            self.away_runs += runs
        else: 
            self.home_runs += runs


class baseball_MCS(): 
    """
    takes in a schedule, simulator, and regressor, iterates through schedule and sims 
    each game, after completing the schedule, it aggregates the data, and starts again
    repeating N times.
    """
    def __init__(self, simulator, regressor, schedule, N=100) -> None:
        self.N = N
        self.simulator = simulator
        self.regressor = regressor
        self.scheduler = schedule

    def run_test(self):
        scores = []
        runs = pd.DataFrame(columns=['gameID', 'date', 'home', 'away', 'winner', 'run_differential'])
        for ep in range(self.N): 
            for game in self.scheduler.iter_test():
                mcs_game = MCS_game(game)
                mcs_game.sim(self.regressor, self.manager, self.simulator) 
            cur_runs = self.scheduler.aggregate()
            runs = pd.concat(runs, cur_runs)
            self.scheduler.reset()
        return runs
    
    def analyze(self, runs): 
        sub_df = runs.groupby(['gameID', 'date','home', 'away']).mean()
        for idx, row in sub_df.iterrows():
            gameID = row[0]
            date = row[1]
            home = row[2]
            away = row[3] 
            winner = row[3] 
            run_diff = row[3] 
            print(f"gameID: {gameID}, date: {date}, home: {home}, away: {away}, win_probability: {winner}, avg_run_differential: {run_diff}")
        