import json
import pandas as pd
from crime.crime_abstract import EditorBase, PrinterBase, ReaderBase, ScraperBase
import googlemaps
from selenium import webdriver
from icecream import ic

class Editor(EditorBase):
    def dropNaN(self, this: pd.DataFrame) -> pd.DataFrame:
        return this.dropna()

class Printer(PrinterBase):
    def print(self, this: pd.DataFrame):
        print('*' * 100)
        ic(f'출력: {type(this)}')
        ic(f'칼럼: {this.columns}')
        ic(f'상위 1개 행: {this.head(1)}')
        ic(f'null 갯수: {this.isnull().sum()} 개')
        print('-' * 100)

class Reader(ReaderBase):
    def __init__(self):
        pass
    
    def print(self, file) -> pd.DataFrame:
        return pd.read_csv(f'{file}', encoding='utf-8', thousands=',')
    
    def print_idx(self, file) -> pd.DataFrame:
        return pd.read_csv(f'{file}', index_col=0, encoding='utf-8', thousands=',')
    
    def xls(self, file, header, usecols) -> pd.DataFrame:
        return pd.read_excel(f'{file}', header=header, usecols=usecols)
    
    def json(self, file) -> pd.DataFrame:
        return json.load(open(f'{file}', encoding='utf-8'))
    
    def gmaps(self, key) -> pd.DataFrame:
        return googlemaps.Client(key=f'{key}')


class Scraper(ScraperBase):
    def __init__(self):
        pass
    
    def driver(self):
        return webdriver.Chrome('C:/Program Files/Google/Chrome/Application/chromedriver.exe')
    
    def auto_login(self, driver, url, selector, data) -> None:
        driver.get(url)
        driver.find_element_by_css_selector(selector).send_keys(data)
        driver.find_element_by_css_selector(selector).submit()