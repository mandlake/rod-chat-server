import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from dotenv import load_dotenv
from konlpy.tag import Kkma, Komoran, Okt, Hannanum
import konlpy
import re
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk import FreqDist
from wordcloud import WordCloud 
import matplotlib.pyplot as plt
from icecream import ic
import tweepy

from crime.crime_util import Reader
from crime.model.data_model import DataModel
from crime.service.data_service import DataService

'''
문제정의 !
서울시의 범죄현황과 CCTV현황을 분석해서
정해진 예산안에서 구별로 다음해에 배분하는 기준을 마련하시오.
예산금액을 입력하면, 구당 할당되는 CCTV 카운터를 자동으로
알려주는 AI 프로그램을 작성하시오.
'''

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

google_key = os.environ['google_map_api_key']

class CrimeReport:
    model = DataModel()
    service = DataService()
    
    def __init__(self):
        this = self.model
        this.cctv = 'cctv_in_seoul.csv'
        this.crime = 'crime_in_seoul.csv'
        self.crime_rate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']
        self.crime_columns = ['살인 발생', '강도 발생', '강간 발생', '절도 발생', '폭력 발생']
        self.arrest_columns = ['살인 검거', '강도 검거', '강간 검거', '절도 검거', '폭력 검거']
        
    def dframe_cctv_idx(self) -> pd.DataFrame:
        return self.service.new_dframe_idx('cctv_in_seoul.csv')
    
    def dframe_cctv(self) -> pd.DataFrame:
        return self.service.new_dframe('cctv_in_seoul.csv')
    
    def dframe_crime(self) -> pd.DataFrame:
        return self.service.new_dframe('crime_in_seoul.csv')
    
    def dframe_pop(self) -> pd.DataFrame:
        return self.service.new_dframe_xls('pop_in_seoul.xls', 2, 'B, D, G, J, N')
    
    def drop_na(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.service.drop_na(df)
    
    def save_police_position(self):
        crime = self.service.new_dframe('crime_in_seoul.csv')
        station_names = []
        for name in crime['관서명']:
            station_names.append('서울' + str(name[:-1]) + '경찰서')
        
        station_address = []
        station_lats = []
        station_lngs = []
        reader = Reader()
        gmaps = reader.gmaps(google_key)
        
        for name in station_names:
            tmp = gmaps.geocode(name, language='ko')
            station_address.append(tmp[0].get("formatted_address"))
            
            tmp_loc = tmp[0].get("geometry")
            station_lats.append(tmp_loc['location']['lat'])
            station_lngs.append(tmp_loc['location']['lng'])
            
        gu_names = []
        for name in station_address:
            tmp = name.split()
            gu_name = [gu for gu in tmp if gu[-1] == '구'][0]
            gu_names.append(gu_name)
        
        crime['구별'] = gu_names
        # 구와 경찰서의 위치가 다른 경우 수작업으로 처리
        crime.loc[crime['관서명'] == '혜화서', ['구별']] = '종로구'
        crime.loc[crime['관서명'] == '서부서', ['구별']] = '은평구'
        crime.loc[crime['관서명'] == '강서서', ['구별']] = '양천구'
        crime.loc[crime['관서명'] == '종암서', ['구별']] = '성북구'
        crime.loc[crime['관서명'] == '방배서', ['구별']] = '서초구'
        crime.loc[crime['관서명'] == '수서서', ['구별']] = '강남구'
        self.service.save_model('police_position.csv', crime)
    
    def save_cctv_pop(self):
        pop = self.dframe_pop()
        cctv = self.dframe_cctv()
        cctv.rename(columns={cctv.columns[0]: '구별'}, inplace=True)
        pop.rename(columns={pop.columns[0]: '구별',
                            pop.columns[1]: '인구수', 
                            pop.columns[2]: '한국인', 
                            pop.columns[3]: '외국인', 
                            pop.columns[4]: '고령자'
                            }, inplace=True)
        
        # pop에서 NULL값이 있는지 확인 후 제거
        pop = self.drop_na(pop)
        pop['외국인비율'] = pop['외국인'] / pop['인구수'] * 100
        pop['고령자비율'] = pop['고령자'] / pop['인구수'] * 100
        cctv.drop(['2013년도 이전', '2014년', '2015년', '2016년'], axis=1, inplace=True)

        # 병합
        cctv_per_pop = pd.merge(cctv, pop, on='구별')
        
        cor1 = np.corrcoef(cctv_per_pop['고령자비율'], cctv_per_pop['소계'])
        cor2 = np.corrcoef(cctv_per_pop['외국인비율'], cctv_per_pop['소계'])
        ic(f'고령자비율과 CCTV의 상관계수 {str(cor1)} \n'
           f'외국인비율과 CCTV의 상관계수 {str(cor2)} ')
        """
         고령자비율과 CCTV 의 상관계수 [[ 1.         -0.28078554]
                                     [-0.28078554  1.        ]] 
         외국인비율과 CCTV 의 상관계수 [[ 1.         -0.13607433]
                                     [-0.13607433  1.        ]]
        r이 -1.0과 -0.7 사이이면, 강한 음적 선형관계,
        r이 -0.7과 -0.3 사이이면, 뚜렷한 음적 선형관계,
        r이 -0.3과 -0.1 사이이면, 약한 음적 선형관계,
        r이 -0.1과 +0.1 사이이면, 거의 무시될 수 있는 선형관계,
        r이 +0.1과 +0.3 사이이면, 약한 양적 선형관계,
        r이 +0.3과 +0.7 사이이면, 뚜렷한 양적 선형관계,
        r이 +0.7과 +1.0 사이이면, 강한 양적 선형관계
        고령자비율 과 CCTV 상관계수 [[ 1.         -0.28078554] 약한 음적 선형관계
                                    [-0.28078554  1.        ]]
        외국인비율 과 CCTV 상관계수 [[ 1.         -0.13607433] 거의 무시될 수 있는
                                    [-0.13607433  1.        ]]                        
         """
        self.service.save_model('cctv_pop.csv', cctv_per_pop)
    
    def save_crime_arrest_normalization(self):
        cctv = self.dframe_cctv()
        police = self.service.new_dframe_save('police_position.csv')
        cctv.rename(columns={cctv.columns[0]: '구별'}, inplace=True)
        
        cctv.drop(['2013년도 이전', '2014년', '2015년', '2016년'], axis=1, inplace=True)
        police.drop(['관서명'], axis=1, inplace=True)
        
        police['범죄발생총합'] = police[self.crime_columns].sum(axis=1)
        police.drop(self.crime_columns, axis=1, inplace=True)
        
        police['검거총합'] = police[self.arrest_columns].sum(axis=1)
        police.drop(self.arrest_columns, axis=1, inplace=True)

        cctv_per_crime = pd.merge(cctv, police, on='구별')
        
        cor1 = np.corrcoef(cctv_per_crime['검거총합'], cctv_per_crime['소계'])
        cor2 = np.corrcoef(cctv_per_crime['범죄발생총합'], cctv_per_crime['소계'])
        ic(f'검거총합과 CCTV의 상관계수 {str(cor1)} \n')
        ic(f'범죄발생총합과 CCTV의 상관계수 {str(cor2)} ')
        
        self.service.save_model('cctv_per_crime.csv', cctv_per_crime)


if __name__ == '__main__':
    crime = CrimeReport()
    crime.save_crime_arrest_normalization()
