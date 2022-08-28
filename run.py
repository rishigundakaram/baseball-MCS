from doctest import master
from yaml import load, FullLoader
import argparse

from model.utils import get_dates
from model.dataset import master_dataset
from model.simulator import Simulator
from model.NCF import NCF

parser = argparse.ArgumentParser(description='Process a run for baseball testing')
parser.add_argument('--config', type=str, help='path to config file')
if __name__ == "__main__": 
    args = parser.parse_args()
    config_file = args.config
    with open(config_file, 'r') as stream: 
        config = load(stream, FullLoader)
    eval = config['eval']
    periods = get_dates(eval['start_date'], eval['periods'], eval['train_window'], eval['test_window'])
    print(periods)
    exit(1)
    database = master_dataset(config['database']['path'])
    for train_start, train_end, test_start, test_end in periods:
        sim = Simulator(train_start, train_end)
        sim.process(database)

        regressor = NCF(database, train_start, train_end, test_start, test_end)
        regressor.train(config['model']['MCS']['regressor'])
        regressor.eval_model()


        exit(1)
    # load the schedule
    # load the model type
    # for each train_period: 
        # get all games before the start date - train_window of weeks
        # train the roster
        # train the regressor if you need
        # train the simulator
        # eval on the test_set
        # send results to wandb

"""
Describing the training data: 
regressor: takes in [pitcher, batter, outcome]
simulator: takes in [current state, outcome, next_state]
roster: takes in [date, game_id, playerID, position, batting order]
"""
    