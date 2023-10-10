import numpy as np
from tqdm.notebook import tqdm
import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
from .utils import outcome
import random



class Multi_Layer_Perceptron(nn.Module):
    def __init__(self, args, num_users, num_items):
        super(Multi_Layer_Perceptron, self).__init__()
        self.num_users = num_users
        self.num_items = num_items
        self.factor_num = args["factor_num"]
        self.layers = [2 * self.factor_num] + args["layers"]
        print(self.factor_num)

        self.embedding_user = nn.Embedding(num_embeddings=self.num_users, embedding_dim=self.factor_num)
        self.embedding_item = nn.Embedding(num_embeddings=self.num_items, embedding_dim=self.factor_num)

        self.fc_layers = nn.ModuleList()
       
        for idx, (in_size, out_size) in enumerate(zip(self.layers[:-1], self.layers[1:])):
            self.fc_layers.append(nn.Linear(in_size, out_size))

        self.affine_output = nn.Linear(in_features=self.layers[-1], out_features=9)
        self.logistic = nn.Sigmoid()

    def forward(self, indices, cur_outs):
        user_indices = indices[:, 0]
        item_indices = indices[:, 1]
        user_embedding = self.embedding_user(user_indices)
        item_embedding = self.embedding_item(item_indices)
        vector = torch.cat([user_embedding, item_embedding, cur_outs], dim=-1)  # the concat latent vector
        for idx, _ in enumerate(range(len(self.fc_layers))):
            vector = self.fc_layers[idx](vector)
            vector = nn.ReLU()(vector)
            # vector = nn.BatchNorm1d()(vector)
            # vector = nn.Dropout(p=0.5)(vector)
        logits = self.affine_output(vector)
        rating = self.logistic(logits)
        return rating



class regressor_dataset(Dataset): 
    def __init__(self, data, pitcher_map, batter_map, outcome_map):
        data = data[["pitcher", "player_id","cur_outs", "outcome"]]

        self.data = torch.zeros((len(data), 3), dtype=torch.long)
        self.target = torch.zeros(len(data), len(self.outcome_map))

        pbar = tqdm(data.itertuples(index=True))
        for row in pbar: 
            cur = [self.pitcher_map[row[1]]], [self.batter_map[row[2]], [row[23]]]
            outcome_idx = self.outcome_map[row[4]]
            self.data[row[0], 0] = torch.tensor([self.pitcher_map[row[1]]])
            self.data[row[0], 1] = torch.tensor([self.batter_map[row[2]]])
            self.data[row[0], 2] = torch.tensor([self.batter_map[row[3]]])
            self.target[row[0], outcome_idx] = 1 
    

    def __len__(self): 
        return self.data.size()[0]

    def __getitem__(self, idx): 
        return self.data[idx, :], self.target[idx, :]


class NCF: 
    def __init__(self, database, train_start, train_end, test_start, test_end) -> None:
        total_df = database.get_plays(train_start, test_end)
        pitchers = total_df["pitcher"].unique()
        batters = total_df["player_id"].unique()
        self.pitcher_map = {id: idx for idx, id in enumerate(pitchers)}
        self.batter_map = {id: idx for idx, id in enumerate(batters)}
        self.outcome_map = {
            "strikeout": 0, 
            "groundout": 1, 
            "flyout": 2, 
            "single": 3, 
            "double": 4, 
            "triple": 5, 
            "homerun": 6, 
            "walk": 7, 
            "other": 8,
        }

        train_df = database.get_plays(train_start, train_end)
        test_df = database.get_plays(test_start, test_end)
        self.train_data = regressor_dataset(train_df, self.pitcher_map, self.batter_map, self.outcome_map)
        self.test_data = regressor_dataset(test_df, self.pitcher_map, self.batter_map, self.outcome_map)
        pass

    def train_model(self, args): 
        train_loader = DataLoader(self.train_data, batch_size=args['batch_size'], shuffle=True)
        self.model = Multi_Layer_Perceptron(args, len(self.pitcher_map), len(self.batter_map))
        optimizer = torch.optim.Adam(self.model.parameters(), lr=args["lr"])
        bce_loss = nn.BCELoss()
        total_iter = len(self.data)/args["batch_size"]
        self.model.train()
        for ep in range(args["epochs"]): 
            losses = []
            iter = 0
            for idxs, outcome in train_loader: 
                optimizer.zero_grad()
                output = self.model(idxs)
                loss = bce_loss(output, outcome)
                loss.backward()
                optimizer.step()
                losses.append(loss)
                iter += 1
                # print(f"percent done: {iter/total_iter*100}%")
            print(f"epoch: {ep}, loss: {round((sum(losses) / len(losses)).item(), 5)}")
    
    def eval_model(self): 
        # Do ROC, brier loss, and cross entropy loss here
        pass

    def predict(self, pitcherID, batterID, cur_outs): 
        data = np.array([self.pitcher_map[pitcherID], self.batter_map[batterID]])
        outs = np.array([[cur_outs]])
        dist = self.model(data, outs)
        outcome = random.choices(outcome.list(), weights=dist)
        return outcome