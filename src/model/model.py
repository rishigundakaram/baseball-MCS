import torch
import torch.nn as nn
import torch.nn.functional as F

class NCF(nn.Module):
    def __init__(self, num_pitchers, num_batters, num_outcomes, embed_dim=50, num_layers=2):
        super(NCF, self).__init__()
        
        # Increase the embedding dimension
        self.pitcher_embedding = nn.Embedding(num_pitchers, embed_dim)
        self.batter_embedding = nn.Embedding(num_batters, embed_dim)
        
        self.fc1 = nn.Linear(embed_dim * 2, 128)  # Increase the hidden layer size
        self.linear_layers = [nn.Linear(128, 128) for _ in range(num_layers-2)]
        self.dropout = [nn.Dropout(.3) for _ in range(num_layers-1)]
        self.output_layer = nn.Linear(128, num_outcomes)
        
        # Add Dropout layers
        self.dropout1 = nn.Dropout(0.3)
        self.dropout2 = nn.Dropout(0.3)
        
    def forward(self, pitcher_ids, batter_ids):
        pitcher_embed = self.pitcher_embedding(pitcher_ids)
        batter_embed = self.batter_embedding(batter_ids)
        
        x = torch.cat([pitcher_embed, batter_embed], dim=1)
    
        x = F.relu(self.fc1(x))
        x = self.dropout[0](x)  # Dropout layer after first hidden layer
        for idx in range(len(self.linear_layers)): 
            x = F.relu(self.linear_layers[idx](x))
            x = self.dropout[idx+1](x)
        
        out = self.output_layer(x)
        
        return out
