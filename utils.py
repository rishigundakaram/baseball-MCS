from enum import Enum

class Pitcher: 
    def __init__(self, stats) -> None:
        stats = stats

class Batter: 
    def __init__(self, stats) -> None:
        stats = stats
        
# State of a baseball game
class State: 
    def __init__(self, pitcher, batter) -> None:
        outs = 0
        a_score = 0
        b_score = 0
        balls = 0
        bases = [0, 0, 0]
        pitcher = pitcher
        batter = batter

class outcome(Enum): 
    out = 1
    strike = 2
    ball = 3
    single = 4
    double = 5
    triple = 6
    homerun = 7

class Transition:
    def sim(self, pitcher, batter) -> outcome: 
        pass
    def next(self, state: State) -> State: 
        return 

class basic_Transition(Transition): 
    

