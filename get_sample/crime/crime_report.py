import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
        
    def dframe_cctv(self) -> object:
        return self.service.new_dframe_idx('cctv_in_seoul.csv')
    
    def dframe_crime(self) -> object:
        return self.service.new_dframe_idx('crime_in_seoul.csv')
    
    def save_police_position(self):
        crime = self.service.new_dframe('crime_in_seoul.csv')
        ic(crime.columns)
        station_names = []
        for name in crime['관서명']:
            station_names.append('서울' + str(name[:-1]) + '경찰서')
        ic(station_names)
        
        station_address = []
        station_lats = []
        station_lngs = []
        reader = Reader()
        gmaps = reader.gmaps(google_key)
        
        for name in station_names:
            tmp = gmaps.geocode(name, language='ko')
            station_address.append(tmp[0].get("formatted_address"))
            
            tmp_loc = tmp[0].get("geometry")
            
            station_address.append(tmp[0].get("formatted_address"))
            station_lats.append(tmp_loc['location']['lat'])
            station_lngs.append(tmp_loc['location']['lng'])
            
        ic(station_address)
        ic(station_lats)
        ic(station_lngs)
    
    def preprocessing(self):
        cctv = self.dframe_cctv()
        crime = self.dframe_crime()
        ic(cctv.columns)
        ic(crime.columns)
    

if __name__ == '__main__':
    crime = CrimeReport()
    crime.save_police_position()