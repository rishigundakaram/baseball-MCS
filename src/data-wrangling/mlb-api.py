import statsapi

def fetch_mlb_play_by_play(date):
    # Get the list of games on the specified date
    schedule = statsapi.schedule(start_date=date, end_date=date, sportId=1)
    
    # Initialize an empty dictionary to store play-by-play data
    all_games_play_by_play = {}
    
    # Loop through each game to fetch the play-by-play data
    for game in schedule:
        game_id = game['game_id']
        play_by_play_data = statsapi.get('game_playByPlay', {'gamePk': game_id})
        
        # Add the play-by-play data to the dictionary, using the game ID as the key
        all_games_play_by_play[game_id] = play_by_play_data
    
    return all_games_play_by_play

def filter_game(game):
     
# Example usage
date = '2023-10-21'  # Replace with the date you are interested in (format: 'YYYY-MM-DD')
play_by_play_data = fetch_mlb_play_by_play(date)
print(play_by_play_data)