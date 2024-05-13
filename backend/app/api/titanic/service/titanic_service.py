from app.api.titanic.model.titanic_model import TitanicModel 
import pandas as pd

class TitanicService:
    model = TitanicModel()
    
    def new_titanic(self, payload) -> object:
        this = self.model
        this.context = './app/api/titanic/data/'
        this.fname = payload
        return pd.read_csv(this.context + this.fname)
    
    def process(self):
        print('프로세스 시작')
        this = self.model
        this.train = self.new_titanic('train.csv')
        this.test = self.new_titanic('test.csv')
        
        self.df_info(this)
        
        this.id = this.test['PassengerId']                          # 승객ID
        this = self.drop_feature(this, 'Name', 'SlbSp', 'Parch', 'Cabin', 'Ticket')
        
        self.df_info(this)
        
        this = self.create_train(this)
    
    @staticmethod
    def df_info(this):
        [print(i.head()) for i in [this.train, this.test]]
        
    @staticmethod
    def create_train(this) -> str:
        return this.train.drop('Survived', axis=1)
    
    @staticmethod
    def create_label(this) -> str:
        return this.train['Survived']
    
    @staticmethod
    def drop_feature(this, *feature) -> object:
        [(i.drop(j, axis=1, inplace=True)) for j in feature for i in [this.train, this.test] if j in i.columns]
        
        return this