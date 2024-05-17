from urllib.request import urlopen

from bs4 import BeautifulSoup

class ScrapBugs:
    
    def __init__(self) -> None:
        pass
    
    def scrap(self) -> list:
        print('벅스 뮤직 사이트에서 데이터를 수집합니다.')
        url = 'https://music.bugs.co.kr/chart/track/realtime/total?' # 크롤링할 사이트 주소
        html_doc = urlopen(url)
        soup = BeautifulSoup(html_doc, 'lxml')
        list1 = self.find_music(soup, 'title')
        list2 = self.find_music(soup, 'artist')
        a = [i if i == 0 or i == 0 else i for i in range(1)]
        b = [i if i == 0 or i == 0 else i for i in []]
        c = [(i, j) for i, j in enumerate([])]
        d = {i : j for i, j in zip(list1, list2)}
        l = [i + j for i, j in zip(list1, list2)]
        l2 = list(zip(list1, list2))
        d1 = dict(zip(list1, list2))
        print(d1)
        return d
    
    def find_music(self, soup: BeautifulSoup, class_name: str) -> list:
        elements = soup.find_all(name='p', attrs={'class': class_name})
        return [element.get_text() for element in elements]
        
if __name__ == '__main__':
    bugs = ScrapBugs()
    bugs.scrap()