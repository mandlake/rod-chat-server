from app.api.titanic.model.titanic_model import TitanicModel 
import pandas as pd

class TitanicService:
    titanic = TitanicModel()
    
    def new_titanic(self, payload) -> object:
        this = self.titanic
        this.context = './data/'
        this.fname = payload
        return pd.read_csv(this.context + this.fname)