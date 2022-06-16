from .transitions import *
from .utils import State

class baseball_MCS(): 
    def __init__(self, game_info, pitcher_info, batter_info, transition=basic_Transition, N=100) -> None:
        self.game_info = game_info
        self.pitcher_info = pitcher_info
        self.batter_info = batter_info
        self.working_state = State(game_info, pitcher_info, batter_info)
        self.N = N
        self.transition = basic_Transition()
    
    def update(self, game_info, pitcher_info, batter_info): 
        self.game_info = game_info
        self.pitcher_info = pitcher_info
        self.batter_info = batter_info
        self.working_state = State(game_info, pitcher_info, batter_info)
        
    def apply_outcomes(self, outcomes): 
        for outcome in outcomes: 
            pass
            # do all the baseball rules here
            # also do all of the manager stuff here
            # change the working state
    
    def sim_game(self): 
        while self.working_state.done is not True: 
            outcomes = self.transition.sim_at_bat(self.working_state)
            self.apply_outcomes(outcomes)
        return self.working_state

    def aggregate(self): 
        # extract info from current working state
        return None

    def run(self):
        scores = []
        for ep in range(self.N): 
            self.sim_game()
            info = self.aggregate()
            scores.append(info)
            self.working_state = State(self.game_info, self.pitcher_info, self.batter_info)
        return scores
