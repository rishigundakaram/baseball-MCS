import pandas as pd
import requests


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
        
    }
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.split(',')
            line = [i[1:-1] for i in line]
            date = line[0]
            visiting_team = line[3]
            home_team = line[6]
            if visiting_team in team_names:
                visiting_team = team_names[visiting_team]
            if home_team in team_names:
                home_team = team_names[home_team]
            data.append({
                'date': pd.to_datetime(date,format='%Y%m%d'),
                'Home': home_team,
                'Away': visiting_team
            })

    df = pd.DataFrame(data)
    return df

def get_team_roster(team_id):
    url = f"https://lookup-service-prod.mlb.com/json/named.roster_40.bam?team_id={team_id}"
    response = requests.get(url)
    data = response.json()
    roster = data["roster_40"]["queryResults"]["row"]

    return roster

# Example usage: Get the current roster of the New York Yankees (team_id = 147)

# Example usage:
if __name__ == '__main__':
    file_path = './data/schedule_2023.txt'
    df = parse_schedule_file(file_path)
    print(df.head())
