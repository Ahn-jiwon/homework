import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 설치 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

Plays=soup.select("#body-content>div.newest-list>div>table>tbody>tr")

# print(len(Plays))
for Play in Plays:
    Rank =Play.select_one('td.number').text[0:2].strip()
    Title=Play.select_one("td.info>a").text.strip()
    Artist=Play.select_one("td.info>a.artist.ellipsis").text
    print(Rank,Title,Artist)
    doc = {
        'Rank': Rank,
        'Title': Title,
        'Artist': Artist  # DB에는 숫자처럼 생긴 문자열 형태로 저장됩니다.
    }
    db.Plays.insert_one(doc)