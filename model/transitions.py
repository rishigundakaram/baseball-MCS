from nis import match
from .utils import outcome, State
from random import choice

class Transition:
    def __init__(self) -> None:
        pass
    def sim_at_bat(self, State): 
        pass

class basic_Transition(Transition): 
    def __init__(self) -> None:
        super().__init__()
    
    def sim_at_bat(self, State):
        event = choice(range(1,8))
        match event: 
            case 1: 
                return [outcome.strikeout]
            case 2: 
                return [outcome.groundout]
            case 3: 
                return [outcome.flyout]
            case 4: 
                return [outcome.single]
            case 5: 
                return [outcome.double]
            case 6: 
                return [outcome.triple]
            case 7: 
                return [outcome.homerun]

