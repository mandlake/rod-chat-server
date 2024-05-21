import os
import sys

import folium
import requests
from sklearn import preprocessing
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

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
        self.crimes_col = ['살인', '강도', '강간', '절도', '폭력']
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
        
        police['살인검거율'] = police['살인 검거'].astype(int) / police['강간 발생'].astype(int) * 100
        police['강도검거율'] = police['강도 검거'].astype(int) / police['강도 발생'].astype(int) * 100
        police['강간검거율'] = police['강간 검거'].astype(int) / police['살인 발생'].astype(int) * 100
        police['절도검거율'] = police['절도 검거'].astype(int) / police['절도 발생'].astype(int) * 100
        police['폭력검거율'] = police['폭력 검거'].astype(int) / police['폭력 발생'].astype(int) * 100
        police.drop(['강간 검거', '강도 검거', '살인 검거', '절도 검거', '폭력 검거'], axis=1, inplace=True)

        for i in self.crime_rate_columns:
            police.loc[police[i] > 100, i] = 100
            
        print('loc 결과 :')
        ic(police)
        
        police.rename(columns={'강간 발생': '강간',
                               '강도 발생': '강도',
                               '살인 발생': '살인',
                               '절도 발생': '절도',
                               '폭력 발생': '폭력'}, inplace=True)
        
        x = police[self.crime_rate_columns].values
        min_max_scalar = preprocessing.MinMaxScaler()
        """     
        피쳐 스케일링(Feature scalining)은 해당 피쳐들의 값을 일정한 수준으로 맞춰주는 것이다.
        이때 적용되는 스케일링 방법이 표준화(standardization) 와 정규화(normalization)다.
        
        1단계: 표준화(공통 척도)를 진행한다.
            표준화는 정규분포를 데이터의 평균을 0, 분산이 1인 표준정규분포로 만드는 것이다.
            x = (x - mu) / sigma
            scale = (x - np.mean(x, axis=0)) / np.std(x, axis=0)
        2단계: 이상치 발견 및 제거
        3단계: 정규화(공통 간격)를 진행한다.
            정규화에는 평균 정규화, 최소-최대 정규화, 분위수 정규화가 있다.
             * 최소최대 정규화는 모든 데이터를 최대값을 1, 최솟값을 0으로 만드는 것이다.
            도메인은 데이터의 범위이다.
            스케일은 데이터의 분포이다.
            목적은 도메인을 일치시키거나 스케일을 유사하게 만든다.     
        """
        x_scaled = min_max_scalar.fit_transform(x.astype(float))
        police_norm = pd.DataFrame(x_scaled, columns=self.crime_rate_columns, index=police.index)
        
        # Make sure '구별' column is included in police_norm
        police_norm['구별'] = police['구별']
    
        police_norm[self.crimes_col] = police[self.crimes_col]
        police_norm['범죄'] = np.sum(police_norm[self.crime_rate_columns], axis=1)
        police_norm['검거'] = np.sum(police_norm[self.crimes_col], axis=1)
        ic(police_norm)
        self.service.save_model('crime_arrest_norm.csv', police_norm)
    
    def folium_test(self):
        state_geo = self.service.new_dframe_json('us-states.json')
        state_data = self.service.new_dframe('us_unemployment.csv')

        m = folium.Map(location=[48, -102], zoom_start=3)

        folium.Choropleth(
            geo_data=state_geo,
            name="choropleth",
            data=state_data,
            columns=["State", "Unemployment"],
            key_on="feature.id",
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Unemployment Rate (%)",
        ).add_to(m)

        folium.LayerControl().add_to(m)
        m.save('./crime/save/us_states.html')
        
        
    def draw_crime_map(self):
        state_geo = self.service.new_dframe_json('kr-states.json')
        state_data = self.service.new_dframe_save('crime_arrest_norm.csv')

        m = folium.Map(location=[37.5502, 126.982], zoom_start=12)

        folium.Choropleth(
            geo_data=state_geo,
            name="choropleth",
            data=tuple(zip(state_data['구별'], state_data['범죄'])),
            columns=["State", "Crime Rate"],
            key_on="feature.id",
            fill_color="PuRd",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Crime Rate (%)",
            reset=True
        ).add_to(m)
        
        for i in state_data.index:
            folium.CircleMarker([state_data['lat'][i], state_data['lng'][i]],
                                radius=state_data['검거'][i] * 10,  # 검거율을 반지름으로 사용
                                color='#3186cc', fill_color='#3186cc').add_to(m)


        folium.LayerControl().add_to(m)
        m.save('./crime/save/kr_states.html')
        
    def jongam_police_info(self):
        return [{'address_components':
                             [{'long_name': '32', 'short_name': '32', 'types': ['premise']},
                              {'long_name': '화랑로7길', 'short_name': '화랑로7길',
                               'types': ['political', 'sublocality', 'sublocality_level_4']},
                              {'long_name': '성북구', 'short_name': '성북구',
                               'types': ['political', 'sublocality', 'sublocality_level_1']},
                              {'long_name': '서울특별시', 'short_name': '서울특별시',
                               'types': ['administrative_area_level_1', 'political']},
                              {'long_name': '대한민국', 'short_name': 'KR', 'types': ['country', 'political']},
                              {'long_name': '100-032', 'short_name': '100-032', 'types': ['postal_code']}],
                         'formatted_address': '대한민국 서울특별시 성북구 화랑로7길 32',
                         'geometry': {'location':
                                          {'lat': 37.60388169879458, 'lng': 127.04001571848704},
                                      'location_type': 'ROOFTOP',
                                      'viewport': {'northeast': {'lat': 37.60388169879458, 'lng': 127.04001571848704},
                                                   'southwest': {'lat': 37.60388169879458, 'lng': 127.04001571848704}}},
                         'partial_match': True, 'place_id': 'ChIJc-9q5uSifDURLhQmr5wkXmc',
                         'plus_code': {'compound_code': 'HX7Q+CV 대한민국 서울특별시', 'global_code': '8Q98HX7Q+CV'},
                         'types': ['establishment', 'point_of_interest', 'police']}]
        

if __name__ == '__main__':
    crime = CrimeReport()
    crime.draw_crime_map()
