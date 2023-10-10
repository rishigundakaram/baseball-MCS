"""
Looking for pitcher and batter statistics vs date. This needs to be computed weekly for 
the model to be accurate. 

TODO: Multiple pitchers with the same name. 
"""
import pandas as pd

# return a nested dictionary with: {year: {name of batter (lastName firstName): batter statistics}}
def parse_id_map(path): 
    df = pd.read_csv(path)
    df = df[['MLBID', 'RETROID', '']]
    return df

def parse_stats(path, id_map: pd.DataFrame, batter=True): 
    headers = []
    years = {}
    with open(path) as f: 
        for line in f: 
            line = line.strip('\n')
            line = line.split(',')
            line = line[:-1]
            if not headers: 
                if batter: 
                    headers = ['batter_' + i for i in line]
                else: 
                    headers = ['pitcher_' + i for i in line]
                headers = headers[4:]
                continue
            sub_df = id_map.loc[id_map['MLBID'] == int(line[2])]
            if sub_df.empty: 
                continue
            retro_id = sub_df.iloc[0]['RETROID']
            cur_year = int(line[3])
            stats = line[4:]
            # ignoring Nans
            if '' in stats: 
                continue
            stats = [float(i) for i in stats]
            if cur_year not in years: 
                years[cur_year] = {retro_id: stats}
            else: 
                years[cur_year][retro_id] = stats
    return headers, years



