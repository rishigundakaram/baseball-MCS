## Baseball MCS

We aim to simulate baseball game outcomes using Monte Carlo simulations.

# Usage

You must use python 3.10. The parsing file can parse EVA and EVA files given by Retrosheet play by play logs it can also get the player name from the player id (Useful for obtaining player statistics later).

To use this package:

- first install anaconda from [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
- run `conda env create -f environment.yml`

# Todo

- Need to finish the simulator. In particular, after a game is simulated what should we keep track of (aggregate function) and how do we go from one state to the next (apply outcomes function)
- Need to finish the dataset creation. Going to have three datasets: player statistics from previous season, game logs (given two teams who won), and dataset of at bats (given a pitcher and a batter, what happened, will be used for more of the machine learning portion).
- Current plan for evaluation is to implement the Brier loss
- Another issue is getting the current team roster. Need a system to get the up to date team roster which could depend on trades
- Long term goals
  - implement other state of the art models and try to see if we can beat them
- testing for the bharathan
