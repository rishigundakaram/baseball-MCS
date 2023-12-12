import streamlit as st
from collections import defaultdict
import pandas as pd

# Import any other necessary modules or functions from your code
# transition_probs = [0.24, 0.37, 0.10, 0.05, 0.137, 0.04, 0.004, .079]
# schedule = parse_schedule_file("../../data/schedule_2023.txt")
# team_rosters = get_all_team_rosters()
# full_season = FullSeason(transition_probs, team_rosters, schedule)
# probabilities = full_season.play_full_season(num_seasons=100)
probabilities = pd.read_csv(
    "https://raw.githubusercontent.com/rishigundakaram/baseball-MCS/main/data/final/probabilities.csv"
)

st.title("MLB World Series Predictions")

st.header("World Series, Division Win, and Playoff Probabilities")

st.write(
    "Here are the probabilities for each team to win the World Series, win their division, and make the playoffs, as well as their average number of wins:"
)

st.dataframe(probabilities)
