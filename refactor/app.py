import streamlit as st
from collections import defaultdict
from parsers import parse_schedule_file
from game import get_all_team_rosters, FullSeason
import pandas as pd
import matplotlib.pyplot as plt


# Import any other necessary modules or functions from your code
transition_probs = [0.24, 0.37, 0.10, 0.05, 0.137, 0.04, 0.004, .079]
schedule = parse_schedule_file("./data/schedule_2023.txt")
team_rosters = get_all_team_rosters()
# full_season = FullSeason(transition_probs, team_rosters, schedule)
# probabilities = full_season.play_full_season(num_seasons=100)
probabilities = pd.read_csv("./data/probabilities.csv")

st.markdown("# MLB World Series Predictions")
st.markdown("### World Series, Division Win, and Playoff Probabilities")
st.markdown("Here are the probabilities for each team to win the World Series, win their division, and make the playoffs, as well as their average number of wins:")

# Coloring the dataframe from white to red based on values
cm = plt.get_cmap('RdYlBu_r')
styled_df = probabilities.style.background_gradient(cmap=cm)

st.dataframe(styled_df)
