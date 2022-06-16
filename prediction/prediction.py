from pandas import DataFrame
from model.simulator import baseball_MCS
from model.transitions import basic_Transition

transition = basic_Transition
model = baseball_MCS(None, None, None, transition)

# get the datasets
game_dataset = None
player_database = None
# for each game in the dataset: 
statistics = DataFrame()
for game in game_dataset:
    pitchers = None # query pitcher statistics using information from game
    batters = None # query batter statistics using information from game 
    # get the current model
    model.update(game, pitchers, batters)
    stats = model.run()
    statistics.update(stats) # update the dataframe with stats

statistics.dump(path) # dump the stats into a bin folder for evaluation later
