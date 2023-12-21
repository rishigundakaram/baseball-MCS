import streamlit as st
from collections import defaultdict
import pandas as pd

# Import any other necessary modules or functions from your code
# transition_probs = [0.24, 0.37, 0.10, 0.05, 0.137, 0.04, 0.004, .079]
# schedule = parse_schedule_file("../../data/schedule_2023.txt")
# team_rosters = get_all_team_rosters()
# full_season = FullSeason(transition_probs, team_rosters, schedule)
# probabilities = full_season.play_full_season(num_seasons=100)


def custom_style():
    st.markdown(
        """
        <style>
        .dataframe-widget .stDataFrame {
            width: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def color_red_gradient(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` proportional to the value.
    """
    red = int(255 * val / 100)
    return f"color: rgb({red}, 0, 0)"


# Apply the styling


def main():
    st.set_page_config(
        page_title="MLB Forecasting", page_icon=":baseball", layout="wide"
    )
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Predictions", "Model Info"])

    if page == "Predictions":
        custom_style()
        probabilities = pd.read_csv(
            "https://raw.githubusercontent.com/rishigundakaram/baseball-MCS/main/data/final/probabilities.csv"
        )
        # probabilities = pd.read_csv(
        #     "/home/projects/baseball-MCS/data/final/probabilities.csv"
        # )
        probabilities = probabilities.drop(probabilities.columns[0], axis=1)
        # probabilities = probabilities.style.applymap(
        #     color_red_gradient,
        #     subset=["Make Playoffs %", "Win Division %", "Win World Series %"],
        # )

        print(probabilities)
        st.title("2024 MLB Season Predictions")

        st.header("World Series, Division Win, and Playoff Probabilities")

        st.write(
            "Here are the probabilities for each team to win the World Series, win their division, and make the playoffs, as well as their average number of wins:"
        )

        st.dataframe(
            probabilities,
            hide_index=True,
            column_config={
                "logo": st.column_config.ImageColumn(label=""),
                "Elo": st.column_config.LineChartColumn(label="Elo"),
            },
        )

    elif page == "Model Info":
        st.title("About the Model")
        st.write("A Blog post about the model")


if __name__ == "__main__":
    main()
