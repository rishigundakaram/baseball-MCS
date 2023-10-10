import pandas as pd
import csv
from pprint import pprint
import re
num_outcomes = 8


def parse_event(event):
    # Split the event into its three main parts.
    parts = re.split(r'[/.]', event)
    print(parts)
    # Basic play.
    basic_play = parts[0]

    # Modifiers.
    modifiers = []
    if len(parts) == 2: 
        modifiers = parts[1]
    elif len(parts) > 2:
        modifiers = parts[1:-1]

    # Runner advances.
    advances = []
    if len(parts) > 2:
        advances = re.split(r'[;]', parts[-1])

    return basic_play, modifiers, advances

def get_outcome(event): 
    basic_play, modifiers, advances = parse_event(event)
    pattern_1 = "\d*"
    if basic_play.isdigit(): 
        print(modifiers)
        # basic play is a hit out
        if any(["L" in i for i in modifiers]): 
            return "linedriveout"
        elif any(["G" in i for i in modifiers]): 
            return "groundout"
        elif any(["F" in i for i in modifiers]): 
            return "flyout"
    
    if "K" in basic_play: return "strikeout"
    if "W" in basic_play or "I" in basic_play: return "walk"
    if "S" in basic_play: return "single"
    if "D" in basic_play: return "double"
    if "T" in basic_play: return "triple"
    if "HR" in basic_play or "H" in basic_play: return "homerun"
    else: return "unknown"


def parse_retrosheet(file):
    all_plays = []
    current_pitcher = {'0': None, '1': None}  
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row_data in reader:
            if row_data[0] == 'id':
                game = {'id': row_data[1], 'plays': []}
                current_pitcher = {'0': None, '1': None} 
            elif row_data[0] == 'start' or row_data[0] == 'sub':  
                if row_data[4] in ['1', '0']:  
                    current_pitcher[row_data[3]] = row_data[1]  
            elif row_data[0] == 'info' and row_data[1] == 'date':
                game['date'] = row_data[2]
            elif row_data[0] == 'play':
                play = {}
                play['inning'] = row_data[1]
                play['team'] = row_data[2]
                play['batter'] = row_data[3]
                play['pitcher'] = current_pitcher[play['team']]
                play['game_id'] = game['id']
                play['date'] = game['date']
                outcome = row_data[6]
                result = get_outcome(outcome)
                if result == "unknown": 
                    print(result)
                    print(outcome)
                    exit(1)
                play['outcome'] = outcome
                all_plays.append(play)

    # Convert the list of all plays into a dataframe
    df = pd.DataFrame(all_plays)

    return df


df = parse_retrosheet('../data/playbyplay/2021eve/2021ANA.EVA')
print(df.head())


import matplotlib.pyplot as plt

# Assuming the column name is 'column_name'
value_counts = df['outcome'].value_counts()

plt.bar(value_counts.index, value_counts.values)
plt.xlabel('Categories')
plt.ylabel('Frequency')
plt.title('Bar Plot of column_name')
plt.xticks(rotation='vertical')  # Rotate x-axis labels if needed
plt.show()


import torch
from torch import nn
from torch.nn import functional as F
from torch.optim import Adam
from torch.utils.data import Dataset, DataLoader

class NeuMF(nn.Module):
    def __init__(self, num_pitchers, num_batters, embedding_size, mlp_units):
        super(NeuMF, self).__init__()
        self.pitcher_embedding = nn.Embedding(num_pitchers, embedding_size)
        self.batter_embedding = nn.Embedding(num_batters, embedding_size)
        self.mlp_layers = nn.ModuleList()
        for units in mlp_units:
            self.mlp_layers.append(nn.Linear(embedding_size*2, units))
            self.mlp_layers.append(nn.ReLU())
            embedding_size = units
        self.final_layer = nn.Linear(embedding_size + 1, num_outcomes)

    def forward(self, pitcher, batter):
        pitcher_vector = self.pitcher_embedding(pitcher)
        batter_vector = self.batter_embedding(batter)
        mf_output = (pitcher_vector * batter_vector).sum(1, keepdim=True)
        mlp_input = torch.cat([pitcher_vector, batter_vector], dim=1)
        mlp_output = mlp_input
        for layer in self.mlp_layers:
            mlp_output = layer(mlp_output)
        model_input = torch.cat([mf_output, mlp_output], dim=1)
        model_output = F.softmax(self.final_layer(model_input), dim=1)
        return model_output


# if __name__ == '__main__': 
    # embedding_size = int(min(len(df['pitcher'].unique()), len(df['batter'].unique())) ** 0.5)
    # mlp_units = [embedding_size * 2, embedding_size]
    # num_outcomes = y.shape[1]

    # model = NeuMF(len(df['pitcher'].unique()), len(df['batter'].unique()), embedding_size, mlp_units)
    # optimizer = Adam(model.parameters())
    # loss_function = nn.CrossEntropyLoss()
