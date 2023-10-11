import random
from collections import defaultdict
import pybaseball as mlb
from datetime import datetime
import pandas as pd
from enum import Enum
from enum import Enum, auto

class League(Enum):
    AMERICAN_LEAGUE = auto()
    NATIONAL_LEAGUE = auto()

class Division(Enum):
    EAST = auto()
    CENTRAL = auto()
    WEST = auto()

class MLBTeam(Enum):
    # American League East
    BALTIMORE_ORIOLES = (110, "BAL", League.AMERICAN_LEAGUE, Division.EAST)
    BOSTON_RED_SOX = (111, "BOS", League.AMERICAN_LEAGUE, Division.EAST)
    NEW_YORK_YANKEES = (147, "NYY", League.AMERICAN_LEAGUE, Division.EAST)
    TAMPA_BAY_RAYS = (139, "TBR", League.AMERICAN_LEAGUE, Division.EAST)
    TORONTO_BLUE_JAYS = (141, "TOR", League.AMERICAN_LEAGUE, Division.EAST)

    # American League Central
    CHICAGO_WHITE_SOX = (145, "CWS", League.AMERICAN_LEAGUE, Division.CENTRAL)
    CLEVELAND_GUARDIANS = (114, "CLE", League.AMERICAN_LEAGUE, Division.CENTRAL)
    DETROIT_TIGERS = (116, "DET", League.AMERICAN_LEAGUE, Division.CENTRAL)
    KANSAS_CITY_ROYALS = (118, "KCR", League.AMERICAN_LEAGUE, Division.CENTRAL)
    MINNESOTA_TWINS = (142, "MIN", League.AMERICAN_LEAGUE, Division.CENTRAL)

    # American League West
    HOUSTON_ASTROS = (117, "HOU", League.AMERICAN_LEAGUE, Division.WEST)
    LOS_ANGELES_ANGELS = (108, "LAA", League.AMERICAN_LEAGUE, Division.WEST)
    OAKLAND_ATHLETICS = (133, "OAK", League.AMERICAN_LEAGUE, Division.WEST)
    SEATTLE_MARINERS = (136, "SEA", League.AMERICAN_LEAGUE, Division.WEST)
    TEXAS_RANGERS = (140, "TEX", League.AMERICAN_LEAGUE, Division.WEST)

    # National League East
    ATLANTA_BRAVES = (144, "ATL", League.NATIONAL_LEAGUE, Division.EAST)
    MIAMI_MARLINS = (146, "MIA", League.NATIONAL_LEAGUE, Division.EAST)
    NEW_YORK_METS = (121, "NYM", League.NATIONAL_LEAGUE, Division.EAST)
    PHILADELPHIA_PHILLIES = (143, "PHI", League.NATIONAL_LEAGUE, Division.EAST)
    WASHINGTON_NATIONALS = (120, "WSN", League.NATIONAL_LEAGUE, Division.EAST)

    # National League Central
    CHICAGO_CUBS = (112, "CHC", League.NATIONAL_LEAGUE, Division.CENTRAL)
    CINCINNATI_REDS = (113, "CIN", League.NATIONAL_LEAGUE, Division.CENTRAL)
    MILWAUKEE_BREWERS = (158, "MIL", League.NATIONAL_LEAGUE, Division.CENTRAL)
    PITTSBURGH_PIRATES = (134, "PIT", League.NATIONAL_LEAGUE, Division.CENTRAL)
    ST_LOUIS_CARDINALS = (138, "STL", League.NATIONAL_LEAGUE, Division.CENTRAL)

    # National League West
    ARIZONA_DIAMONDBACKS = (109, "ARI", League.NATIONAL_LEAGUE, Division.WEST)
    COLORADO_ROCKIES = (115, "COL", League.NATIONAL_LEAGUE, Division.WEST)
    LOS_ANGELES_DODGERS = (119, "LAD", League.NATIONAL_LEAGUE, Division.WEST)
    SAN_DIEGO_PADRES = (135, "SD", League.NATIONAL_LEAGUE, Division.WEST)
    SAN_FRANCISCO_GIANTS = (137, "SF", League.NATIONAL_LEAGUE, Division.WEST)

team_abbrev_to_enum = {
    "BAL": MLBTeam.BALTIMORE_ORIOLES,
    "BOS": MLBTeam.BOSTON_RED_SOX,
    "NYY": MLBTeam.NEW_YORK_YANKEES,
    "TBR": MLBTeam.TAMPA_BAY_RAYS,
    "TOR": MLBTeam.TORONTO_BLUE_JAYS,
    "CWS": MLBTeam.CHICAGO_WHITE_SOX,
    "CLE": MLBTeam.CLEVELAND_GUARDIANS,
    "DET": MLBTeam.DETROIT_TIGERS,
    "KCR": MLBTeam.KANSAS_CITY_ROYALS,
    "MIN": MLBTeam.MINNESOTA_TWINS,
    "HOU": MLBTeam.HOUSTON_ASTROS,
    "LAA": MLBTeam.LOS_ANGELES_ANGELS,
    "OAK": MLBTeam.OAKLAND_ATHLETICS,
    "SEA": MLBTeam.SEATTLE_MARINERS,
    "TEX": MLBTeam.TEXAS_RANGERS,
    "ATL": MLBTeam.ATLANTA_BRAVES,
    "MIA": MLBTeam.MIAMI_MARLINS,
    "NYM": MLBTeam.NEW_YORK_METS,
    "PHI": MLBTeam.PHILADELPHIA_PHILLIES,
    "WSN": MLBTeam.WASHINGTON_NATIONALS,
    "CHC": MLBTeam.CHICAGO_CUBS,
    "CIN": MLBTeam.CINCINNATI_REDS,
    "MIL": MLBTeam.MILWAUKEE_BREWERS,
    "PIT": MLBTeam.PITTSBURGH_PIRATES,
    "STL": MLBTeam.ST_LOUIS_CARDINALS,
    "ARI": MLBTeam.ARIZONA_DIAMONDBACKS,
    "COL": MLBTeam.COLORADO_ROCKIES,
    "LAD": MLBTeam.LOS_ANGELES_DODGERS,
    "SD": MLBTeam.SAN_DIEGO_PADRES,
    "SF": MLBTeam.SAN_FRANCISCO_GIANTS
}

class BaseballGame:
    def __init__(self, transition_probs, home_team, away_team):
        self.transition_probs = transition_probs
        # require home and away teams to be Rosters of players
        self.home_team = home_team
        self.away_team = away_team
        self.inning = 1
        self.outs = 0
        self.home_score = 0
        self.away_score = 0
        self.bases = [0,0,0]
        self.home_batting_order = 0
        self.away_batting_order = 0

    def simulate_inning(self):
        self.outs = 0
        self.bases = [0, 0, 0]
        batting_order = self.away_batting_order
        while self.outs < 3:
            outcome = random.choices(
                population=['strikeout', 'groundout', 'flyout', 'single', 'double', 'triple', 'homerun', 'walk'],
                weights=self.transition_probs,
                k=1
            )[0]

            if outcome == 'strikeout' or outcome == 'groundout' or outcome == 'flyout':
                self.outs += 1
            else:
                self.bases[0], self.bases[1], self.bases[2], outs, runs = self.update_bases(outcome)
                self.outs += outs
                self.away_score += runs

            batting_order = (batting_order + 1) % len(self.away_team)
        self.away_batting_order = batting_order

        batting_order = self.home_batting_order
        self.outs = 0
        self.bases = [0, 0, 0]
        while self.outs < 3:
            outcome = random.choices(
                population=['strikeout', 'groundout', 'flyout', 'single', 'double', 'triple', 'homerun', 'walk'],
                weights=self.transition_probs,
                k=1
            )[0]

            if outcome == 'strikeout' or outcome == 'groundout' or outcome == 'flyout':
                self.outs += 1
            else:
                self.bases[0], self.bases[1], self.bases[2], outs, runs = self.update_bases(outcome)
                self.outs += outs
                self.home_score += runs

            batting_order = (batting_order + 1) % len(self.home_team)
        self.home_batting_order = batting_order


    def update_bases(self, outcome):
        outs = 0
        runs = 0
        bases = self.bases
        if outcome == 'single': 
            if bases[2] == 1: 
                runs += 1
            bases[0] = 1
            bases[1] = self.bases[0]
            bases[2] = bases[1]
        elif outcome == 'double': 
            if bases[2] == 1: 
                runs += 1
            if bases[1] == 1: 
                runs += 1
            bases[0] = 0
            bases[1] = 1
            bases[2] = bases[1]
        elif outcome == 'triple': 
            if bases[2] == 1: 
                runs += 1
            if bases[1] == 1: 
                runs += 1
            if bases[0] == 1:  
                runs += 1
            bases[2] = 1
        elif outcome == 'homerun': 
            runs += sum(bases)
            bases = [0, 0, 0]
        return *bases, outs, runs

    def play(self):
        while self.inning <= 9 or (self.inning > 9 and self.home_score == self.away_score):
            self.simulate_inning()
            self.inning += 1


from collections import defaultdict

class Season:
    def __init__(self, transition_probs, team_rosters, schedule):
        self.transition_probs = transition_probs
        self.team_rosters = team_rosters
        self.schedule = schedule

    def play_seasons(self, num_seasons=1):
        global team_abbrev_to_enum
        standings = {
            League.AMERICAN_LEAGUE: {
                Division.EAST: defaultdict(lambda: {"wins": 0, "losses": 0}),
                Division.CENTRAL: defaultdict(lambda: {"wins": 0, "losses": 0}),
                Division.WEST: defaultdict(lambda: {"wins": 0, "losses": 0}),
            },
            League.NATIONAL_LEAGUE: {
                Division.EAST: defaultdict(lambda: {"wins": 0, "losses": 0}),
                Division.CENTRAL: defaultdict(lambda: {"wins": 0, "losses": 0}),
                Division.WEST: defaultdict(lambda: {"wins": 0, "losses": 0}),
            }
        }

        for _ in range(num_seasons):
            for game in self.schedule.itertuples():
                home_team = team_abbrev_to_enum[game.Home]
                away_team = team_abbrev_to_enum[game.Away]
                game_result = self.play_game(game.Home, game.Away)
                home_league = home_team.value[2]
                away_league = away_team.value[2]
                home_division = home_team.value[3]
                away_division = away_team.value[3]

                if game_result["winner"] == "home":
                    standings[home_league][home_division][game_result["home_team"]]["wins"] += 1
                    standings[away_league][away_division][game_result["away_team"]]["losses"] += 1
                else:
                    standings[home_league][home_division][game_result["home_team"]]["losses"] += 1
                    standings[away_league][away_division][game_result["away_team"]]["wins"] += 1

        return standings

    def play_game(self, home_team_abbr, away_team_abbr):
        global team_abbrev_to_enum
        home_team = team_abbrev_to_enum[home_team_abbr]
        away_team = team_abbrev_to_enum[away_team_abbr]

        home_roster = self.team_rosters[home_team_abbr]
        away_roster = self.team_rosters[away_team_abbr]

        game = BaseballGame(self.transition_probs, home_roster, away_roster)
        game.play()

        winner = "home" if game.home_score > game.away_score else "away"
        return {"winner": winner, "home_team": home_team, "away_team": away_team}

class Postseason:
    def __init__(self, transition_probs, team_rosters, nl_div_winners, al_div_winners, nl_wildcards, al_wildcards):
        self.transition_probs = transition_probs
        self.team_rosters = team_rosters
        self.nl_div_winners = nl_div_winners
        self.al_div_winners = al_div_winners
        self.nl_wildcards = nl_wildcards
        self.al_wildcards = al_wildcards

    def play_series(self, team1, team2, num_games):
        team1_wins = 0
        team2_wins = 0
        team1_roster = self.team_rosters[team1.value[1]]
        team2_roster = self.team_rosters[team2.value[1]]
        while team1_wins < num_games // 2 + 1 and team2_wins < num_games // 2 + 1:
            game = BaseballGame(self.transition_probs, team1_roster, team2_roster)
            game.play()
            if game.home_score > game.away_score:
                team1_wins += 1
            else:
                team2_wins += 1

        return team1 if team1_wins > team2_wins else team2

    def play_postseason(self):
        # Wild Card games
        nl_wildcard_winner = self.play_series(self.nl_wildcards[0][0], self.nl_wildcards[1][0], 3)
        al_wildcard_winner = self.play_series(self.al_wildcards[0][0], self.al_wildcards[1][0], 3)

        # Division Series
        nl_div_series_1 = self.play_series(self.nl_div_winners[Division.WEST], nl_wildcard_winner, 5)
        nl_div_series_2 = self.play_series(self.nl_div_winners[Division.EAST], self.nl_div_winners[Division.CENTRAL], 5)

        al_div_series_1 = self.play_series(self.al_div_winners[Division.WEST], al_wildcard_winner, 5)
        al_div_series_2 = self.play_series(self.al_div_winners[Division.EAST], self.al_div_winners[Division.CENTRAL], 5)

        # Championship Series
        nl_champion = self.play_series(nl_div_series_1, nl_div_series_2, 7)
        al_champion = self.play_series(al_div_series_1, al_div_series_2, 7)

        # World Series
        world_series_champion = self.play_series(nl_champion, al_champion, 7)
        return world_series_champion

class FullSeason:
    def __init__(self, transition_probs, team_rosters, schedule):
        self.transition_probs = transition_probs
        self.team_rosters = team_rosters
        self.schedule = schedule
    def init_results(self): 
        results = {}
        for team in MLBTeam:
            results[team] = {"division_wins": 0, "playoff_appearances": 0, "world_series_wins": 0, "total_games_won": 0}
        return results
    
    def play_full_season(self, num_seasons=1):
        results = self.init_results()

        for i in range(num_seasons):
            season = Season(self.transition_probs, self.team_rosters, self.schedule)
            season_results = season.play_seasons(1)

            division_winners, wildcards = self.get_playoff_teams(season_results)

            for league in division_winners:
                for winner in division_winners[league]:
                    team_name = winner[0]
                    results[team_name]["division_wins"] += 1
                    results[team_name]["playoff_appearances"] += 1
                    results[team_name]["total_games_won"] += winner[1]["wins"]

            for league in wildcards:
                for wildcard in wildcards[league]:
                    team_name = wildcard[0]
                    results[team_name]["playoff_appearances"] += 1
                    results[team_name]["total_games_won"] += wildcard[1]["wins"]

            postseason = Postseason(self.transition_probs, self.team_rosters,
                                    division_winners[League.NATIONAL_LEAGUE],
                                    division_winners[League.AMERICAN_LEAGUE],
                                    wildcards[League.NATIONAL_LEAGUE],
                                    wildcards[League.AMERICAN_LEAGUE],)
            world_series_winner = postseason.play_postseason()
            results[world_series_winner]["world_series_wins"] += 1
            print(f"iteration {i} complete")
        # Calculate probabilities and average number of games won
        for team_name, data in results.items():
            data["division_win_prob"] = data["division_wins"] / num_seasons
            data["playoff_appearance_prob"] = data["playoff_appearances"] / num_seasons
            data["world_series_win_prob"] = data["world_series_wins"] / num_seasons
            data["avg_games_won"] = data["total_games_won"] / num_seasons

        return results

    
    def get_playoff_teams(self, standings):
        division_winners = {
            League.AMERICAN_LEAGUE: [],
            League.NATIONAL_LEAGUE: [],
        }
        wildcards = {
            League.AMERICAN_LEAGUE: [],
            League.NATIONAL_LEAGUE: [],
        }
        
        for league in standings:
            all_teams = []
            for division in standings[league]:
                # Sort teams in division by wins (descending)
                sorted_teams = sorted(standings[league][division].items(), key=lambda x: x[1]['wins'], reverse=True)
                # Get division winner
                division_winner = sorted_teams[0]
                division_winners[league].append(division_winner)
                
                # Add other teams to the list for wildcards
                all_teams.extend(sorted_teams[1:])
            
            # Sort all_teams by wins (descending) and get the top three teams as wildcards
            all_teams_sorted = sorted(all_teams, key=lambda x: x[1]['wins'], reverse=True)
            wildcards[league] = all_teams_sorted[:3]
        return division_winners, wildcards



from parsers import parse_schedule_file, get_team_roster

def get_all_team_rosters():
    rosters = {}
    for team in MLBTeam:
        team_id = team.value[0]
        team_abbr = team.value[1]
        roster = get_team_roster(team_id)
        rosters[team_abbr] = roster

    return rosters

def extract_dataframe(probabilities): 
    team_data = []
    for team, stats in probabilities.items():
        if team is not None:
            team_data.append(
                [
                    team.name,
                    stats["world_series_win_prob"],
                    stats["division_win_prob"],
                    stats["playoff_appearance_prob"],
                    stats["avg_games_won"],
                ]
            )
    columns = [
        "Team",
        "World Series Win Probability",
        "Division Win Probability",
        "Playoff Appearance Probability",
        "Average Games Won",
    ]
    team_data.sort(key=lambda x: x[1], reverse=True)
    team_data = pd.DataFrame(team_data, columns=columns)
    return team_data
if __name__ == '__main__':
    transition_probs = [0.24, 0.37, 0.10, 0.05, 0.137, 0.04, 0.004, .079]
    schedule = parse_schedule_file("./data/schedule_2023.txt")
    team_rosters = get_all_team_rosters()
    full_season = FullSeason(transition_probs, team_rosters, schedule)
    probabilities = full_season.play_full_season(num_seasons=1)
    team_data = extract_dataframe(probabilities)
    team_data.to_csv("./data/probabilities.csv")


