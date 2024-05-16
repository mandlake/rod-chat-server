import pandas as pd
from app.api.domain.data_sets import DataSets

class models :
    def __init__(self) -> None:
        self.ds = DataSets()
        this = self.ds
        this.dname = './app/api/titanic/data/'
        this.sname = './app/api/titanic/save/'
        
    def new_dataframe_with_index(self, fname: pd.DataFrame) -> pd.DataFrame:
        this = self.ds
        return pd.read_csv(f'{this.dname}{fname}', index_col=0)
    
    def new_dataframe_no_index(self, fname: pd.DataFrame) -> pd.DataFrame:
        this = self.ds
        return pd.read_csv(f'{this.dname}{fname}')
    
    def save_model(self, fname, dframe: pd.DataFrame) -> pd.DataFrame:
        this = self.ds
        '''
        풀옵션은 다음과 같다.
        df.to_csv(f'{self.ds.sname}{fname}',sep=',',na_rep='NaN',
                         float_format='%.2f',  # 2 decimal places
                         columns=['ID', 'X2'],  # columns to write
                         index=False)  # do not write index
        '''
        return dframe.to_csv(f'{this.sname}{fname}', sep=',', na_rep='NaN')