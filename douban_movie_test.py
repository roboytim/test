import requests
import json
import re
from bs4 import BeautifulSoup

def getSummary(url):
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    return(soup.select('.indent span')[-1].text.strip())
res = requests.get('https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=20')
res.encoding = 'utf-8'
#print(res.text)
#print(type(res.text))
jd = json.loads(res.text)
for i in range(len(jd['subjects'])):
    print(jd['subjects'][i]['rate'],jd['subjects'][i]['title'],jd['subjects'][i]['url'],getSummary(jd['subjects'][i]['url']))
