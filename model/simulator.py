from doctest import master
import torch
from .dataset import master_dataset
from .utils import outcome

class Simulator(): 
    def __init__(self, start_date, end_date, factors=None, representation_bases='Full') -> None:
        self.factors = factors
        self.representation_bases = representation_bases
        self.start_date = start_date
        self.end_date = end_date

    def process(self,db: master_dataset): 
        self.core = db.get_transitions(self.start_date, self.end_date)
    
    def sample(self, outcome=outcome.strikeout, outs=0, first=0, second=0, third=0): 
        """
        returns 5 integers, the first three denote whether the bases are filled, the fourth
        is the number of outs after the play, and the last is the number of runs scored
        """
        print(self.core)
        sub_df = self.core[
            (self.core['outcome'] == outcome.name) & 
            (self.core['pre_outs'] == outs) & 
            (self.core['pre_1'] == first) & 
            (self.core['pre_2'] == second) & 
            (self.core['pre_3'] == third)
            ]
        print(sub_df)
        row = sub_df.sample(1)
        row = row[['post_1', 'post_2', 'post_3', 'post_outs', 'runs']]
        return row.values[0]
    

        
