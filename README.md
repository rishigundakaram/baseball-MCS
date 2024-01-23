## Baseball Monte Carlo Forecasting

# Overview

This repository contains the code for this [website](https://bball-forecasting.streamlit.app/). On the website you will find a projections of all the MLB teams. Some stats of interest to you may be their projected amount of wins, the probability they make it to the playoffs, and the probability they win the World Series

# How Does it work?

Calculating these probabilities rely on a technique known as Monte Carlo Forecasting. If you are unfamiliar and want to learn more see the [Wikipedia](https://en.wikipedia.org/wiki/Monte_Carlo_method). There are two main componenets to the system. One is developing a model that given a matchup between two teams, will give a probability of either team winning. The second is using these probabilities, randomly sampling thousands of seasons. Across all the seasons we simulate we can count the number of wins, number of times made the playoffs, number of times won the world series for each team, then by averaging we can get associated probabilites.

# Todo

- Need to finish the simulator. In particular, after a game is simulated what should we keep track of (aggregate function) and how do we go from one state to the next (apply outcomes function)
- Need to finish the dataset creation. Going to have three datasets: player statistics from previous season, game logs (given two teams who won), and dataset of at bats (given a pitcher and a batter, what happened, will be used for more of the machine learning portion).
- Current plan for evaluation is to implement the Brier loss
- Another issue is getting the current team roster. Need a system to get the up to date team roster which could depend on trades
- Long term goals
  - implement other state of the art models and try to see if we can beat them
- testing for the bharathan
- Need to implement Manager class, and analysis of results
