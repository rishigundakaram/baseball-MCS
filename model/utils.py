from enum import Enum

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
        

        



