import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

from crime.model.data_model import DataModel
from crime.service.data_service import DataService


class CrimeReport:
    model = DataModel()
    service = DataService()
    
    def __init__(self):
        this = self.model
    
    def preprocessing(self) -> object:
        this = self.model
        this.cctv = self.service.new_dframe_idx('cctv_in_seoul.csv')
        print(f'cctv: {this.cctv.head(2)}')
        this.crime = self.service.new_dframe_idx('crime_in_seoul.csv')
        print(f'crime: {this.crime.head(2)}')
    

if __name__ == '__main__':
    crime = CrimeReport()
    crime.preprocessing()
        
        
        