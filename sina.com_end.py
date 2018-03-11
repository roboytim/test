import requests
from bs4 import  BeautifulSoup
from datetime import datetime
import json
import re
import pandas
#----------------------------------------------------------------------------
#获取新闻评论数的方法
commentURL='http://comment5.news.sina.com.cn/page/info?version=1&format=json&channel=gn&newsid=comos-{}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3&t_size=3&h_size=3&thread=1'
def getCommentCounts(newsurl):
    m = re.search('doc-i(.*).shtml',newsurl)
    newsid = m.group(1)
    comments = requests.get(commentURL.format(newsid))
    jd = json.loads(comments.text.strip('var data='))
    return jd['result']['count']['total']
#获取新闻正文信息，包括评论信息
def getNewsDetail(newsurl):
    result = {}
    res = requests.get(newsurl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    result['title'] = soup.select('.main-title')[0].text
    result['newssource'] = soup.select('.date-source a')[0].text
    timesource = soup.select('.date-source')[0].contents[1].text.strip()
    result['dt'] = datetime.strptime(timesource,'%Y年%m月%d日 %H:%M')
    result['article'] = '\n'.join([p.text.strip() for p in soup.select('.article p')[:-1]])
    result['editor'] = soup.select('.show_author')[0].text.lstrip('责任编辑：')
    result['comments'] = getCommentCounts(newsurl)
    return result
def parseListLinks(url):
    newsdatails = []
    res = requests.get(url)
    jd = json.loads(res.text.lstrip('  newsloadercallback(').rstrip(');'))
    for ent in jd['result']['data']:
        newsdatails.append(getNewsDetail(ent['url']))
    return newsdatails
url = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}'
news_total = []
for i in range(1,3):
    newsurl = url.format(i)
    newsary = parseListLinks(newsurl)
    news_total.extend(newsary)
df = pandas.DataFrame(news_total)
#输出前十条新闻，不填数据，默认输出前五条
#print(df.head(10))
df.to_excel(r'C:\Users\Tim.Robert\Desktop\test\news.xlsx')