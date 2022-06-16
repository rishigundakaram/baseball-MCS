from enum import Enum
# use stackprinter for debugging
# import stackprinter
# stackprinter.set_excepthook(style='darkbg2') 


class Pitcher: 
    def __init__(self, stats) -> None:
        stats = stats

class Batter: 
    def __init__(self, stats) -> None:
        stats = stats
        
# State of a baseball game
class Game: 
    def __init__(self, pitcher: Pitcher, batter: Batter) -> None:
        outs = 0
        offense = None
        defense = None
        inning = 1
        balls = 0
        strikes = 0
        bases = [0, 0, 0]
        pitcher = pitcher
        batter = batter
        done = False

    def simulate(self, transition: Transition):
        outcomes = transition.sim_at_bat(self.pitcher, self.batter)
        for outcome in outcomes: 
            # apply the rules of the game when three outs occur
        return None

class outcome: 
    def __init__(self, code) -> None:
        match code: 
            case: 1
                code
    out = 1
    strike = 2
    ball = 3
    single = 4
    double = 5
    triple = 6
    homerun = 7

    def apply(self, game: Game): 
        

class Transition:
    def sim_at_bat(self, pitcher: Pitcher, batter: Batter) -> outcome: 
        pass
    def next(self, state: Game) -> Game: 
        return 

class basic_Transition(Transition): 
    def sim_at_bat(self, pitcher, batter) -> outcome:
        super().sim_at_bat(pitcher, batter)


