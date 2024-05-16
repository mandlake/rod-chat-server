import pandas as pd
from app.api.domain.data_sets import DataSets

class models :
    def __init__(self) -> None:
        self.ds = DataSets()
        this = self.ds
        this.dname = './data'
        this.sname = './save'
        
    def new_model(self, payload) -> object:
        this = self.ds
        this.fname = payload
        return pd.read_csv(f'{this.dname}{this.fname}', index_col=0)
    
    def new_dframe(self, fname) -> object:
        this = self.ds
        return pd.DataFrame(f'{this.dname}{fname}')
    
    def save_model(self, fname, dfname) -> object:
        this = self.ds
        '''
        풀옵션은 다음과 같다.
        df.to_csv(f'{self.ds.sname}{fname}',sep=',',na_rep='NaN',
                         float_format='%.2f',  # 2 decimal places
                         columns=['ID', 'X2'],  # columns to write
                         index=False)  # do not write index
        '''
        this.train.to_csv(f'{this.sname}{fname}', sep=',', na_rep='NaN')