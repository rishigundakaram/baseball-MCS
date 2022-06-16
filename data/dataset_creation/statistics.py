"""
Looking for pitcher and batter statistics vs date. This needs to be computed weekly for 
the model to be accurate. 

TODO: Multiple pitchers with the same name. 
"""

# return a nested dictionary with: {year: {name of batter (lastName firstName): batter statistics}}
def parse_stats(path, batter=True): 
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
            cur_name = line[1].strip() + ' ' + line[0]
            cur_year = line[3]
            stats = line[4:]
            if '' in stats: 
                continue
            stats = [float(i) for i in stats]
            if cur_year not in years: 
                years[cur_year] = {cur_name: stats}
            else: 
                if cur_name in years[cur_year]: 
                    print(cur_year)
                    print(f'repeated name: {cur_name}')
                years[cur_year][cur_name] = stats
    return headers, years



