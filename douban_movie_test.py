import requests
import json
import pandas
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
    result['title']=soup.select('#content span')[0].text
    result['score']=soup.select('.ll')[1].text
    result['summary']=getSummary(url)
    return result
def movieList(url):
    moviedetails=[]
    res=requests.get(url)
    jd = json.loads(res.text)
    for i in range(len(jd['subjects'])):
        moviedetails.append(MovieDetail(jd['subjects'][i]['url']))
    return moviedetails
url='https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start={}'
movietotal=[]
for i in range(1,3):
    movieurl = url.format(20*i)
    moviearry = movieList(movieurl)
    movietotal.extend(moviearry)
df = pandas.DataFrame(movietotal)
print(len(df))