from crime.model.data_model import DataModel
import pandas as pd

class DataService:
    def __init__(self):
        self.data = DataModel()
        this = self.data
        this.dname = './crime/data/'
    
    def new_dframe_idx(self, fname: str) -> object:
        this = self.data
        return pd.read_csv(f'{this.dname}{fname}', index_col=0)
    
    def new_dframe(self, fname: str) -> object:
        this = self.data
        return pd.read_csv(f'{this.dname}{fname}')