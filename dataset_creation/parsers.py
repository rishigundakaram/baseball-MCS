def parse_id(game, lst): 
    game['home_team'] = lst[1][:3]
    game['date'] = lst[1][3:]

def parse_info(game, lst): 
    game[lst[1]] = lst[2]

def parse_start_sub(game, lst):
    lst[5] = int(lst[5])
    lst[3] = int(lst[3])
    if lst[5] == 1: 
        if lst[3] == 0:
            game['cur_pitcher_visit'] = lst[1]
        if lst[3] == 1:
            game['cur_pitcher_home'] = lst[1]

# Todo: Figure out which outcomes are important and parse through them
def parse_outcome(play): 
    return play 

# play = [inning, cur_pitcher, cur_batter, num_pitches thrown, outcome]
def parse_play(game,lst): 
    lst[2] = int(lst[2])
    lst[1] = int(lst[1])
    cur_pitcher = game['cur_pitcher_home'] if lst[2] == 1 else game['cur_pitcher_visit']
    num_pitches = -99 if lst[5] == '' else len(lst[5])
    outcome = parse_outcome(lst[6])
    play = [lst[1], cur_pitcher, lst[3], num_pitches, outcome]
    game['plays'].append(play)

# Takes in path to EVX file and returns list of dicts. Each element in list is a game. Keys
# and values are parsed based on functions above. plays are stored as a list of each play. 
def parse_EVX(path): 
    all_games = []
    first = 1
    with open(path) as f:
        for line in f: 
            line = line.strip('\n')
            line = line.split(',')
            
            match line[0]:
                case 'id': 
                    if not first: 
                        all_games.append(cur_game)
                    first = 0
                    cur_game = {'plays': []}
                    parse_id(cur_game, line)
                case 'info': 
                    parse_info(cur_game, line)
                case 'start': 
                    parse_start_sub(cur_game, line)
                case 'sub': 
                    parse_start_sub(cur_game, line)
                case 'play': 
                    parse_play(cur_game, line)
    return all_games

# Takes in path of retrosheet ids and returns dict with keys as ids and values as 
# [lastName, firstName]
def parse_names(path): 
    players = {}
    with open(path) as f: 
        for line in f: 
            line = line.strip('\n')
            line = line.split(',')
            players[line[0]] = [line[1], line[2]]
    return players


def parse_game_log(path):
    games = []
    with open(path) as f: 
        for line in f: 
            line = line[:-1]
            line = line.split(',')

            for idx in range(len(line)): 
                if line[idx][0] == '\"': 
                    line[idx] = line[idx][1:-1]
                else: 
                    line[idx] = int(line[idx])
            print(line)
            if line[0] == "20210403": 
                exit(1)
