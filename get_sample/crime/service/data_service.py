from context.model.data_model import DataModel
import pandas as pd

from crime.crime_util import Editor, Reader


class DataService:
    def __init__(self):
        self.data = DataModel()
        self.reader = Reader()
        self.editor = Editor()
        this = self.data
        this.dname = './crime/data/'
        this.sname = './crime/save/'

    def get_sname(self):
        return self.data.sname
    
    def drop_na(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.editor.dropNaN(df)

    def new_dframe_idx(self, fname: str) -> pd.DataFrame:
        this = self.data
        # index_col=0 해야 기존 index 값이 유지된다
        # 0은 컬럼명 중 첫번째를 의미한다(배열구조)
        # pd.read_csv('경로/파일명.csv', index_col = '인덱스로 지정할 column명') Index 지정
        return self.reader.print_idx(f'{this.dname}{fname}')
    
    def new_dframe(self, fname: str) -> pd.DataFrame:
        return self.reader.print(f'{self.data.dname}{fname}')
    
    def new_dframe_save(self, fname: str) -> pd.DataFrame:
        return self.reader.print_idx(f'{self.data.sname}{fname}')
    
    def new_dframe_xls(self, fname: str, header, usecols) -> pd.DataFrame:
        return self.reader.xls(f'{self.data.dname}{fname}', header, usecols)

    def save_model(self, fname: str, dframe: pd.DataFrame):
        this = self.data
        '''
        풀옵션은 다음과 같다
        df.to_csv(f'{self.data.sname}{fname}',sep=',',na_rep='NaN',
                         float_format='%.2f',  # 2 decimal places
                         columns=['ID', 'X2'],  # columns to write
                         index=False)  # do not write index
        '''
        dframe.to_csv(f'{this.sname}{fname}', sep=',', na_rep='NaN')