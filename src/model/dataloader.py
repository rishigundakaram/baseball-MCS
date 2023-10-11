import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import json

class PlaysDataset(Dataset):
    def __init__(self, df, pitcher_encoder, batter_encoder, outcome_encoder):
        self.pitcher_encoder = pitcher_encoder
        self.batter_encoder = batter_encoder
        self.outcome_encoder = outcome_encoder
        
        self.pitchers = self.pitcher_encoder.transform(df['pitcher'])
        self.batters = self.batter_encoder.transform(df['batter'])
        self.outcomes = self.outcome_encoder.transform(df['outcome'])
        
    def __len__(self):
        return len(self.pitchers)
    
    def __getitem__(self, idx):
        return self.pitchers[idx], self.batters[idx], self.outcomes[idx]


