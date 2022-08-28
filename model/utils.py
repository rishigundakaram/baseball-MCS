from ast import walk
from enum import Enum
from datetime import date, timedelta, datetime
from tracemalloc import start

from traitlets import All

# use stackprinter for debugging
# import stackprinter
# stackprinter.set_excepthook(style='darkbg2') 
        
# State of a baseball game
class State: 
    def __init__(self, pitcher, batter) -> None:
        outs = 0
        home_runs = 0
        away_runs = 0
        offense = None
        defense = None
        inning = 1
        bases = [0, 0, 0]
        pitcher = pitcher
        batter = batter
        done = False
    
class outcome(Enum): 
    strikeout = 1
    groundout = 2
    flyout = 3
    single = 4
    double = 5
    triple = 6
    homerun = 7
    walk = 8

# ignores substitutions
class Roster:
    def __init__(self, team, window=4) -> None:
        self.team = team
        self.window = window
        self.batters = None
        # df of [date, gameid, starting_pitcher_id]
        self.starting_pitchers = None
        self.relievers = None
        pass
    
    def sample_batting_lineup(self): 
        pass
    def sample_reliever(self): 
        pass

        
def get_dates(start_date, periods, train_window='Full', test_window='Full'):
    """
    Given the start date of the testing, number of periods, and the window of train data
    and test data, return a list of length number of periods with elements: 
    [train_start_date, train_end_date, test_start_date, test_end_date]
    """
    times = []
    test_start_date = datetime.strptime(str(start_date), '%m/%d/%Y')
    for i in range(periods): 
        cur_test_start_date = test_start_date + timedelta(weeks=test_window*i)
        if test_window != 0:  
            cur_test_end_date = test_start_date + timedelta(weeks=test_window)
        else: 
            cur_test_end_date = date.today()
    
        
        if train_window != 0:  
            cur_train_start_date = cur_test_start_date - timedelta(weeks=train_window)
        else: 
            cur_train_start_date = datetime.strptime('04/01/2001', '%m/%d/%Y')

        cur_train_end_date = cur_test_start_date - timedelta(days=1)
        
        times.append([
            cur_train_start_date.strftime('%Y-%m-%d'), 
            cur_train_end_date.strftime('%Y-%m-%d'), 
            cur_test_start_date.strftime('%Y-%m-%d'), 
            cur_test_end_date.strftime('%Y-%m-%d'),
            ])
    return times

        



