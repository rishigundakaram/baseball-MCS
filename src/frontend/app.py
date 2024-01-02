import streamlit as st
from collections import defaultdict
import pandas as pd
from datetime import datetime
from datetime import timedelta

# import strptime

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


import re
import requests


def extract_date_from_filename(filename):
    pattern = r"(\d{4}_\d{2}_\d{2})"
    match = re.search(pattern, filename)
    return match.group(1) if match else None


def get_files_and_dates(repo, path):
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    response = requests.get(url)
    files_dates = {}

    if response.status_code == 200:
        files = response.json()
        for file in files:
            if file["type"] == "file":
                date = extract_date_from_filename(file["name"])
                if date:
                    files_dates[file["name"]] = date
    else:
        print("Failed to retrieve repository data")

    return files_dates


# Apply the styling
def convert_date(date):
    date = date.replace("_", "/")
    return date[5:] + "/" + date[:4]


def main():
    st.set_page_config(
        page_title="MLB Forecasting", page_icon=":baseball", layout="wide"
    )
    repo = "rishigundakaram/baseball-MCS"
    path = "data/final"
    files_dates = get_files_and_dates(repo, path)
    dates = list(files_dates.values())
    dates.sort(reverse=True)
    input_date = st.date_input("Choose a date", value=None)
    # given an input date, find the closest date in the list of dates
    date = min(
        dates,
        key=lambda x: max(
            datetime.strptime(convert_date(x), "%m/%d/%Y").date() - input_date,
            timedelta(days=0),
        ),
    )

    filename = [k for k, v in files_dates.items() if v == date][0]
    probabilities = pd.read_csv(
        f"https://raw.githubusercontent.com/{repo}/main/{path}/{filename}"
    )

    custom_style()
    # probabilities = pd.read_csv(
    #     "https://raw.githubusercontent.com/rishigundakaram/baseball-MCS/main/data/final/2023_02_01probabilities.csv"
    # )
    # probabilities = pd.read_csv(
    #     "/home/projects/baseball-MCS/data/final/probabilities.csv"
    # )
    probabilities = probabilities.drop(probabilities.columns[0], axis=1)
    # probabilities = probabilities.style.applymap(
    #     color_red_gradient,
    #     subset=["Make Playoffs %", "Win Division %", "Win World Series %"],
    # )
    season = date[:4]
    st.title(f"{season} Season MLB Predictions")

    st.dataframe(
        probabilities,
        hide_index=True,
        column_config={
            "logo": st.column_config.ImageColumn(label=""),
            "Elo": st.column_config.LineChartColumn(label="Elo"),
        },
    )
    # italicize and right align the date of the predictions
    st.markdown(
        f"<p style='text-align: right; font-style: italic;'>Predictions from {convert_date(date)}</p>",
        unsafe_allow_html=True,
    )
    # st.write(f"Predictions From {convert_date(date)}")
    st.divider()
    st.subheader("Blog Posts")
    medium_blog_url = "https://medium.com/@rishi.gundakaram/baseball-forecasting-using-monte-carlo-simulation-f789ba0abee2"
    st.markdown(f"[How Are These Probabilities Calculated?]({medium_blog_url})")


if __name__ == "__main__":
    main()
