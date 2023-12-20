import json
from game import BaseballGame
from collections import defaultdict
from datetime import datetime, timedelta
from collections import deque
from stats import Analyzer
from static import MLBTeams
from alive_progress import alive_bar
from collections import defaultdict


def default_game_tracking():
    return deque([])


class LatestGameData:
    def __init__(self) -> None:
        self.tracking_static = defaultdict(default_game_tracking)
        self.tracking_sim = defaultdict(default_game_tracking)

    def update(self, game, sim=False):
        if sim:
            tracking = self.tracking_sim
        else:
            tracking = self.tracking_static
        tracking[game.home_team].append([game.home_batting_order, game.home_sp])
        if len(tracking[game.home_team]) > 5:
            tracking[game.home_team].popleft()

        tracking[game.away_team].append([game.away_batting_order, game.away_sp])
        if len(tracking[game.away_team]) > 5:
            tracking[game.away_team].popleft()

    def reset(self):
        self.tracking_sim = defaultdict(default_game_tracking)

    def get(self, team):
        # get the latest batting order, and the starting pitcher from 5 games ago
        num_games = len(self.tracking_sim[team])
        if num_games == 0:
            batting_order = self.tracking_static[team][-1][0]
            sp = self.tracking_static[team][0][1]
        elif num_games == 5:
            batting_order = self.tracking_sim[team][-1][0]
            sp = self.tracking_sim[team][0][1]
        else:
            batting_order = self.tracking_sim[team][-1][0]
            sp = self.tracking_static[team][num_games][1]
        return batting_order, sp


def default_standings():
    return {"wins": 0, "losses": 0}


class Standings:
    def __init__(self):
        global MLBTeams
        self.MLBTeams = MLBTeams
        self.standings_static = self.init_standings()
        self.standings_sim = self.init_standings()

    def init_standings(self):
        return {
            "AL": {
                "E": defaultdict(default_standings),
                "C": defaultdict(default_standings),
                "W": defaultdict(default_standings),
            },
            "NL": {
                "E": defaultdict(default_standings),
                "C": defaultdict(default_standings),
                "W": defaultdict(default_standings),
            },
        }

    def update_standings(self, game, sim=True):
        if sim:
            standings = self.standings_sim
        else:
            standings = self.standings_static
        home_team, away_team = game.home_team, game.away_team
        home_league, away_league = (
            self.MLBTeams[home_team]["league"],
            self.MLBTeams[away_team]["league"],
        )
        home_division, away_division = (
            self.MLBTeams[home_team]["division"],
            self.MLBTeams[away_team]["division"],
        )
        if game.home_score > game.away_score:
            winner_league, winner_division, winner_team = (
                home_league,
                home_division,
                home_team,
            )
            loser_league, loser_division, loser_team = (
                away_league,
                away_division,
                away_team,
            )
        else:
            loser_league, loser_division, loser_team = (
                home_league,
                home_division,
                home_team,
            )
            winner_league, winner_division, winner_team = (
                away_league,
                away_division,
                away_team,
            )

        standings[winner_league][winner_division][winner_team]["wins"] += 1
        standings[loser_league][loser_division][loser_team]["losses"] += 1

    def combine_standings(self):
        """Combines static and simulated standings."""
        combined_standings = self.init_standings()

        for league in ["AL", "NL"]:
            for division in ["E", "C", "W"]:
                # Combine teams from both static and simulated standings
                all_teams = set(self.standings_static[league][division]) | set(
                    self.standings_sim[league][division]
                )

                for team in all_teams:
                    static_wins = (
                        self.standings_static[league][division][team]["wins"]
                        if team in self.standings_static[league][division]
                        else 0
                    )
                    static_losses = (
                        self.standings_static[league][division][team]["losses"]
                        if team in self.standings_static[league][division]
                        else 0
                    )

                    sim_wins = (
                        self.standings_sim[league][division][team]["wins"]
                        if team in self.standings_sim[league][division]
                        else 0
                    )
                    sim_losses = (
                        self.standings_sim[league][division][team]["losses"]
                        if team in self.standings_sim[league][division]
                        else 0
                    )

                    combined_standings[league][division][team]["wins"] = (
                        static_wins + sim_wins
                    )
                    combined_standings[league][division][team]["losses"] = (
                        static_losses + sim_losses
                    )

        return combined_standings

    def calculate_seeds(self):
        """Calculates playoff seeds based on combined standings."""
        combined_standings = self.combine_standings()

        # Calculate division winners and wild card teams
        division_winners = defaultdict(dict)
        wild_card_teams = defaultdict(list)

        for league in ["AL", "NL"]:
            for division in combined_standings[league]:
                # Determine the division winner
                division_teams = combined_standings[league][division]
                division_winner = max(
                    division_teams,
                    key=lambda team: (
                        division_teams[team]["wins"],
                        -division_teams[team]["losses"],
                    ),
                )
                division_winners[league][division] = division_winner

            # Prepare a list of teams excluding division winners
            league_teams = [
                team
                for division in combined_standings[league]
                for team in combined_standings[league][division]
                if team not in division_winners[league].values()
            ]

            # Sort and select wild card teams
            sorted_wild_cards = sorted(
                league_teams,
                key=lambda team: (
                    combined_standings[league][self.MLBTeams[team]["division"]][team][
                        "wins"
                    ],
                    -combined_standings[league][self.MLBTeams[team]["division"]][team][
                        "losses"
                    ],
                ),
                reverse=True,
            )
            wild_card_teams[league] = sorted_wild_cards[:3]

        # Calculate seeds
        seeds = defaultdict(dict)
        for league in ["AL", "NL"]:
            # Sort division winners to assign seeds 1, 2, 3
            sorted_division_winners = sorted(
                division_winners[league].items(),
                key=lambda item: (
                    combined_standings[league][item[0]][item[1]]["wins"],
                    -combined_standings[league][item[0]][item[1]]["losses"],
                ),
                reverse=True,
            )
            for i, (division, team) in enumerate(sorted_division_winners):
                seeds[league][i + 1] = team

            # Assign seeds 4, 5, 6 to wild card teams
            for i, team in enumerate(wild_card_teams[league]):
                seeds[league][i + 4] = team

        return seeds

    def reset(self):
        self.standings_sim = self.init_standings()

    def __str__(self) -> str:
        combined_standings = self.combine_standings()
        print(combined_standings)
        return f"standings: str(combined_standings)"


# TODO: add in support for mid-post season play
class FullSeason:
    def __init__(self, year, simulator, latest_game_data, is_complete=True) -> None:
        self.year = year
        self.reg_season_complete = []
        self.reg_season_to_sim = []
        # {team: stack([{batting_order, starting_pitcher}]) -> stack always max len(5   )}
        self.LatestGameData = latest_game_data
        self.simulator = simulator
        self.standings = Standings()
        pass

    def __len__(self):
        return len(self.reg_season_complete) + len(self.reg_season_to_sim)

    def add_game(self, game, before_cuttoff=True) -> None:
        if game["regular_season"] and before_cuttoff:
            self.reg_season_complete.append(BaseballGame(game, to_sim=False))
        elif game["regular_season"] and not before_cuttoff:
            self.reg_season_to_sim.append(BaseballGame(game, to_sim=True))

    def prep(self):
        self.reg_season_complete = sorted(
            self.reg_season_complete,
            key=lambda x: datetime.strptime(x.date, "%Y/%m/%d"),
        )
        self.reg_season_to_sim = sorted(
            self.reg_season_to_sim,
            key=lambda x: datetime.strptime(x.date, "%Y/%m/%d"),
        )

        for game in self.reg_season_complete:
            self.LatestGameData.update(game, sim=False)
            self.standings.update_standings(game, sim=False)
            self.simulator.train(game)

    def get_is_complete(self):
        return (len(self.reg_season_to_sim)) == 0

    def reset(self):
        for game in self.reg_season_to_sim:
            game.reset()
        self.LatestGameData.reset()
        self.standings.reset()

    def sim(self):
        for game in self.reg_season_to_sim:
            self.simulator.sim(game)
            self.standings.update_standings(game, sim=True)
            self.LatestGameData.update(game, sim=True)
            last_date = game.date

        # calculate the standings
        seeds = self.standings.calculate_seeds()
        # sim playoffs
        outcome = self.sim_postseason(seeds, start_date=last_date)
        return self.standings, seeds, outcome

    def sim_postseason(self, seeds, start_date):
        # first round series
        start_date = datetime.strptime(start_date, "%Y/%m/%d")
        nl_wildcard_winner = self.play_series(
            seeds["NL"][4], seeds["NL"][5], 3, start_date
        )
        nl_third_seed_winner = self.play_series(
            seeds["NL"][3], seeds["NL"][6], 3, start_date
        )
        diff = timedelta(days=7)
        start_date = start_date + diff

        al_wildcard_winner = self.play_series(
            seeds["AL"][4], seeds["AL"][5], 3, start_date
        )
        al_third_seed_winner = self.play_series(
            seeds["AL"][3], seeds["AL"][6], 3, start_date
        )
        diff = timedelta(days=7)
        start_date = start_date + diff

        # second round series
        nl_div_series_1 = self.play_series(
            seeds["NL"][2], nl_third_seed_winner, 5, start_date
        )
        nl_div_series_2 = self.play_series(
            seeds["NL"][1], nl_wildcard_winner, 5, start_date
        )
        diff = timedelta(days=7)
        start_date = start_date + diff

        al_div_series_1 = self.play_series(
            seeds["AL"][2], al_third_seed_winner, 5, start_date
        )
        al_div_series_2 = self.play_series(
            seeds["AL"][1], al_wildcard_winner, 5, start_date
        )
        diff = timedelta(days=7)
        start_date = start_date + diff

        # Championship Series
        nl_champion = self.play_series(nl_div_series_1, nl_div_series_2, 7, start_date)
        al_champion = self.play_series(al_div_series_1, al_div_series_2, 7, start_date)
        diff = timedelta(days=7)
        start_date = start_date + diff

        # World Series
        world_series_champion = self.play_series(
            nl_champion, al_champion, 7, start_date
        )
        return world_series_champion

    def play_series(self, home, away, num_games, start_date):
        home_wins = 0
        away_wins = 0
        while home_wins < num_games // 2 + 1 and away_wins < num_games // 2 + 1:
            home_batting_order, home_sp = self.LatestGameData.get(home)
            away_batting_order, away_sp = self.LatestGameData.get(away)
            diff = timedelta(days=home_wins + away_wins + 1)
            date = start_date + diff
            game = {
                "home_team": home,
                "away_team": away,
                "home_batting_order": home_batting_order,
                "away_batting_order": away_batting_order,
                "home_sp": home_sp,
                "away_sp": away_sp,
                "date": date.strftime("%Y/%m/%d"),
            }
            game = self.simulator.sim(BaseballGame(game, to_sim=True))
            if game.home_score > game.away_score:
                home_wins += 1
            else:
                away_wins += 1
            self.LatestGameData.update(game, sim=True)

        return home if home_wins > away_wins else away


# TODO: Add functionality to deal with simulating playoffs during the playoffs
class Schedule:
    def __init__(self, all_games_path, data_stop_date, simulator) -> None:
        data_stop_date = datetime.strptime(data_stop_date, "%Y/%m/%d")

        with open(all_games_path, "r") as f:
            all_games = json.load(f)
        self.latest_game_data = LatestGameData()
        self.all_games = all_games
        self.seasons = {}
        # add all games to correct SeasonBlocks
        for game in all_games:
            date = datetime.strptime(game["date"], "%Y/%m/%d")

            year = date.year
            is_complete = date < data_stop_date

            if year not in self.seasons:
                self.seasons[year] = FullSeason(
                    year, simulator, self.latest_game_data, is_complete=is_complete
                )

            before_cuttoff = date <= data_stop_date
            if game["regular_season"]:
                self.seasons[year].add_game(game, before_cuttoff=before_cuttoff)

        self.start_year = min(self.seasons.keys())
        self.end_year = max(self.seasons.keys())
        self.seasons = [
            self.seasons[i] for i in range(self.start_year, self.end_year + 1)
        ]

    def check(self):
        assert self.seasons[-1].get_is_complete() == False
        num_complete = 0
        for season in self.seasons[:-1]:
            assert season.get_is_complete == True

    def prep(self):
        for season in self.seasons:
            season.prep()

    def sim(
        self,
        analyzer,
        n=1,
    ):
        self.prep()
        with alive_bar(n) as bar:
            for i in range(n):
                self.seasons[-1].reset()
                standings, seeds, outcome = self.seasons[-1].sim()
                analyzer.update(standings, seeds, outcome)
                bar()
        return analyzer


from sim import RandomSimulator
from pprint import pprint

if __name__ == "__main__":
    all_games_path = "/home/projects/baseball-MCS/data/intermediate/all_games.json"
    data_stop_date = "2023/04/01"
    simulator = RandomSimulator()
    schedule = Schedule(all_games_path, data_stop_date, simulator)
    n = 1000
    analyzer = Analyzer(n=n)
    analyzer = schedule.sim(analyzer, n=n)
    out = analyzer.export()
    out.to_csv("/home/projects/baseball-MCS/data/final/temp_probabilities.csv")
    print(out)
