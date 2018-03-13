import requests
import json
import pandas
import demjson
from bs4 import BeautifulSoup

def getSummary(url):
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    summary=soup.select('#link-report span')[-1].text.strip().replace('\n','').replace(' ','').replace('　　','')
    if summary=='©豆瓣':
        summary=soup.select('#link-report span')[:-1][-1].text.strip().replace('\n','').replace(' ','').replace('　　','')
    return summary
def MovieDetail(url):
    result={}
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    result['title']=soup.select('#content span')[0].text.strip()
    result['score']=soup.select('.ll')[1].text
    result['summary']=getSummary(url)
    return result
def movieList(url):
    moviedetails=[]
    res=requests.get(url)
    #resend=demjson.encode(res.text)
    soup=BeautifulSoup(res.text,'html.parser')
    for i in range(len(soup.select('.pl2 a'))):
        moviedetails.append(MovieDetail(soup.select('.pl2 a')[i]['href']))
    return moviedetails
url='https://movie.douban.com/chart'
movietotal=[]
movietotal.extend(movieList(url))
df = pandas.DataFrame(movietotal)
#print(df.head())
df.sort_values(by='score',ascending=False).to_excel(r'/Users/roboytim/Desktop/movies.xlsx')