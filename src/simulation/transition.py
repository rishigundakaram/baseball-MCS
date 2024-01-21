import torch
from torch.autograd import Variable
import random


class TransitionModel:
    def sample(self, pitcher_id, batter_id):
        raise NotImplementedError


class RandomTransitionModel(TransitionModel):
    def __init__(self) -> None:
        super().__init__()
        self.transition_probs = [0.24, 0.37, 0.10, 0.05, 0.137, 0.04, 0.004, 0.079]

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


class NCFTransitionModel(TransitionModel):
    def __init__(self, ncf_model, pitcher_encoder, batter_encoder, outcome_encoder):
        self.ncf_model = ncf_model
        self.ncf_model.eval()
        self.pitcher_encoder = pitcher_encoder
        self.batter_encoder = batter_encoder
        self.outcome_encoder = outcome_encoder
        self.ncf_model = ncf_model
        self.ncf_model.eval()

    def sample(self, pitcher_id, batter_id):
        pitcher_id_tensor = Variable(torch.LongTensor([pitcher_id]))
        batter_id_tensor = Variable(torch.LongTensor([batter_id]))

        predicted_outcomes = self.ncf_model(pitcher_id_tensor, batter_id_tensor)
        predicted_outcomes = (
            torch.softmax(predicted_outcomes, dim=1).detach().numpy()[0]
        )

        return predicted_outcomes
