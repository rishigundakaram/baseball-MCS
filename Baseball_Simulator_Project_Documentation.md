  # Baseball Simulator Project Documentation

## Introduction

This documentation provides an in-depth overview of the Baseball Simulator Project, covering its structure, classes, and key functionalities.

## Simulation Module

### __init__.py

#### Significant Code Blocks:




### game.py

#### Significant Code Blocks:

```python
class League(Enum):
    AMERICAN_LEAGUE = auto()
    NATIONAL_LEAGUE = auto()
```
```python
class Division(Enum):
    EAST = auto()
    CENTRAL = auto()
    WEST = auto()
```
```python
class MLBTeam(Enum):
    # American League East
    BALTIMORE_ORIOLES = (110, "BAL", League.AMERICAN_LEAGUE, Division.EAST)
    BOSTON_RED_SOX = (111, "BOS", League.AMERICAN_LEAGUE, Division.EAST)
    NEW_YORK_YANKEES = (147, "NYY", League.AMERICAN_LEAGUE, Division.EAST)
    TAMPA_BAY_RAYS = (139, "TBR", League.AMERICAN_LEAGUE, Division.EAST)
    TORONTO_BLUE_JAYS = (141, "TOR", League.AMERICAN_LEAGUE, Division.EAST)
```
```python
    def __init__(
        self,
        TransitionModel,
        home_team,
        away_team,
    ):
        self.TransitionModel = TransitionModel
        # require home and away teams to be Rosters of players
        self.home_team = home_team
        self.away_team = away_team
        self.inning = 1
        self.outs = 0
        self.home_score = 0
        self.away_score = 0
        self.bases = [0, 0, 0]
        self.home_batting_order = 0
        self.away_batting_order = 0
        self.home_sp = 
```
```python
    def simulate_inning(self):
        self.outs = 0
        self.bases = [0, 0, 0]
        batting_order = self.away_batting_order
        while self.outs < 3:
            pitcher = 
            outcome = self.TransitionModel.sample()
```
```python
    def update_bases(self, outcome):
        outs = 0
        runs = 0
        bases = self.bases
        if outcome == "single":
            if bases[2] == 1:
                runs += 1
            bases[0] = 1
            bases[1] = self.bases[0]
            bases[2] = bases[1]
        elif outcome == "double":
            if bases[2] == 1:
                runs += 1
            if bases[1] == 1:
                runs += 1
            bases[0] = 0
            bases[1] = 1
            bases[2] = bases[1]
        elif outcome == "triple":
            if bases[2] == 1:
                runs += 1
            if bases[1] == 1:
                runs += 1
            if bases[0] == 1:
                runs += 1
            bases[2] = 1
        elif outcome == "homerun":
            runs += sum(bases)
            bases = [0, 0, 0]
        return *bases, outs, runs
```
```python
    def play(self):
        while self.inning <= 9 or (
            self.inning > 9 and self.home_score == self.away_score
        ):
            self.simulate_inning()
            self.inning += 1
```
```python
    def __init__(self, transition_probs, team_rosters, schedule):
        self.transition_probs = transition_probs
        self.team_rosters = team_rosters
        self.schedule = schedule
```
```python
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
            },
        }
```
```python
    def play_game(self, home_team_abbr, away_team_abbr):
        global team_abbrev_to_enum
        home_team = team_abbrev_to_enum[home_team_abbr]
        away_team = team_abbrev_to_enum[away_team_abbr]
```
```python
    def __init__(
        self,
        transition_probs,
        team_rosters,
        nl_div_winners,
        al_div_winners,
        nl_wildcards,
        al_wildcards,
    ):
        self.transition_probs = transition_probs
        self.team_rosters = team_rosters
        self.nl_div_winners = nl_div_winners
        self.al_div_winners = al_div_winners
        self.nl_wildcards = nl_wildcards
        self.al_wildcards = al_wildcards
```
```python
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
```
```python
    def play_postseason(self):
        # Wild Card games
        nl_wildcard_winner = self.play_series(
            self.nl_wildcards[0][0], self.nl_wildcards[1][0], 3
        )
        al_wildcard_winner = self.play_series(
            self.al_wildcards[0][0], self.al_wildcards[1][0], 3
        )
```
```python
    def __init__(self, transition_probs, team_rosters, schedule):
        self.transition_probs = transition_probs
        self.team_rosters = team_rosters
        self.schedule = schedule
```
```python
    def init_results(self):
        results = {}
        for team in MLBTeam:
            results[team] = {
                "division_wins": 0,
                "playoff_appearances": 0,
                "world_series_wins": 0,
                "total_games_won": 0,
            }
        return results
```
```python
    def play_full_season(self, num_seasons=1):
        results = self.init_results()
```
```python
    def get_playoff_teams(self, standings):
        division_winners = {
            League.AMERICAN_LEAGUE: [],
            League.NATIONAL_LEAGUE: [],
        }
        wildcards = {
            League.AMERICAN_LEAGUE: [],
            League.NATIONAL_LEAGUE: [],
        }
```
```python
def get_all_team_rosters():
    rosters = {}
    for team in MLBTeam:
        team_id = team.value[0]
        team_abbr = team.value[1]
        roster = get_team_roster(team_id)
        rosters[team_abbr] = roster
```
```python
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
```


### parsers.py

#### Significant Code Blocks:

```python
def parse_schedule_file(file_path):
    team_names = {
        'CHN': 'CHC',
        'CHA': 'CWS',
        'KCA': 'KCR',
        'LAN': 'LAD',
        'NYN': 'NYM',
        'NYA': 'NYY',
        'SFN': 'SF',
        'ANA': 'LAA',
        'SDN': 'SD',
        'SLN': 'STL',
        'TBA': 'TBR', 
        'WAS': 'WSN', 
```
```python
def get_team_roster(team_id):
    url = f"https://lookup-service-prod.mlb.com/json/named.roster_40.bam?team_id={team_id}"
    response = requests.get(url)
    data = response.json()
    roster = data["roster_40"]["queryResults"]["row"]
```


### sim.py

#### Significant Code Blocks:




### transition.py

#### Significant Code Blocks:

```python
    def sample(self, pitcher_id, batter_id):
        raise NotImplementedError
```
```python
    def __init__(self) -> None:
        super().__init__()
        self.transition_probs = [0.24, 0.37, 0.10, 0.05, 0.137, 0.04, 0.004, 0.079]
```
```python
    def sample(self, pitcher_id, batter_id):
        outcome = random.choices(
            population=[
                "strikeout",
                "groundout",
                "flyout",
                "single",
                "double",
                "triple",
                "homerun",
                "walk",
            ],
            weights=self.transition_probs,
            k=1,
        )[0]
        return outcome
```
```python
    def __init__(self, ncf_model, pitcher_encoder, batter_encoder, outcome_encoder):
        self.ncf_model = ncf_model
        self.ncf_model.eval()
        self.pitcher_encoder = pitcher_encoder
        self.batter_encoder = batter_encoder
        self.outcome_encoder = outcome_encoder
        self.ncf_model = ncf_model
        self.ncf_model.eval()
```
```python
    def sample(self, pitcher_id, batter_id):
        pitcher_id_tensor = Variable(torch.LongTensor([pitcher_id]))
        batter_id_tensor = Variable(torch.LongTensor([batter_id]))
```


## Model Module

### __init__.py

#### Significant Code Blocks:




### dataloader.py

#### Significant Code Blocks:

```python
    def __init__(self, df, pitcher_encoder, batter_encoder, outcome_encoder):
        self.pitcher_encoder = pitcher_encoder
        self.batter_encoder = batter_encoder
        self.outcome_encoder = outcome_encoder
```
```python
    def __len__(self):
        return len(self.pitchers)
```


### EVX_parsing.py

#### Significant Code Blocks:

```python
def parse_id(game, lst):
    game["home_team"] = lst[1][:3]
    game["date"] = lst[1][3:]
```
```python
def parse_info(game, lst):
    game[lst[1]] = lst[2]
```
```python
def parse_start_sub(game, lst):
    lst[5] = int(lst[5])
    lst[3] = int(lst[3])
    if lst[5] == 1:
        if lst[3] == 0:
            game["cur_pitcher_visit"] = lst[1]
        if lst[3] == 1:
            game["cur_pitcher_home"] = lst[1]
        if lst[0] == "start":
            if lst[3] == 0:
                game["visit_sp"] = lst[1]
            if lst[3] == 1:
                game["home_sp"] = lst[1]
```
```python
def parse_EVX(path):
    all_games = []
    first = 1
    with open(path) as f:
        for line in f:
            line = line.strip("\n")
            line = line.split(",")
```
```python
def parse_outcome(outcome_code):
    outcome_mapping = {
        "K": "strikeout",
        "S": "single",
        "D": "double",
        "T": "triple",
        "H": "homerun",
        "W": "walk",
        "GO": "groundout",
        "FO": "flyout",
        "HP": "walk",  # Hit by Pitch, categorized as a walk
        "/G": "groundout",
        "/F": "flyout",
        "/L": "lineout",
        "/P": "popout",
    }
```
```python
def parse_play(game, lst):
    lst[2] = int(lst[2])
    lst[1] = int(lst[1])
    cur_pitcher = game["cur_pitcher_home"] if lst[2] == 1 else game["cur_pitcher_visit"]
    num_pitches = -99 if lst[5] == "" else len(lst[5])
    outcome = parse_outcome(lst[6])
    play = {
        "inning": lst[1],
        "pitcher": cur_pitcher,
        "batter": lst[3],
        "num_pitches": num_pitches,
        "outcome": outcome,
        "raw_outcome": lst[6],
    }
    if "plays" not in game:
        game["plays"] = []
    game["plays"].append(play)
```
```python
def analyze_outcomes(games):
    outcome_counter = Counter()
    total_plays = 0
    total_games = len(games)
```
```python
def identify_unknown_codes(games):
    unknown_codes = Counter()
```
```python
def aggregate_EVX_files(root_directory):
    all_games = []
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith(".EVA") or file.endswith(".EVN"):
                file_path = os.path.join(root, file)
                games = parse_EVX(file_path)
                all_games.extend(games)
    return all_games
```
```python
def EVX_json_to_csv(path):
    with open(path, "r") as f:
        all_games = json.load(f)
```


### model.py

#### Significant Code Blocks:

```python
    def __init__(
        self, num_pitchers, num_batters, num_outcomes, embed_dim=50, num_layers=2
    ):
        super(NCF, self).__init__()
```
```python
    def forward(self, pitcher_ids, batter_ids):
        pitcher_embed = self.pitcher_embedding(pitcher_ids)
        batter_embed = self.batter_embedding(batter_ids)
```


### train.py

#### Significant Code Blocks:

```python
def evaluate_model(test_loader, model):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    all_preds = []
    all_labels = []
    all_probabilities = []
```


## Frontend Module

### __init__.py

#### Significant Code Blocks:




### app.py

#### Significant Code Blocks:



