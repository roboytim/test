import requests
from bs4 import  BeautifulSoup
from datetime import datetime
import json
import re
res = requests.get('http://news.sina.com.cn/china/')
#输出响应码200
#print (res)
#输出res的默认编码格式
#print (res.encoding)
#更改res的编码方式为UTF-8
res.encoding = 'utf-8'
#输出文本内容
#print (res.text)
soup =BeautifulSoup(res.text,'html.parser')
#print(type(soup))
#按照 .news-item标签提取内容信息，在class中，前面加.
for news in soup.select('.news-item'):
    #去掉h2中内容为空的，为空时len为0
    if(len(news.select('h2'))>0):
        h2 = news.select('h2')[0].text
        time  = news.select('.time')[0].text
        a = news.select('a')[0]['href']
        #print (time,h2,a)
#获取新闻正文
res2 = requests.get('http://news.sina.com.cn/c/2018-03-10/doc-ifyscrpm0408106.shtml')
res2.encoding = 'utf-8'
#print (res2.text)
soup2 = BeautifulSoup(res2.text,'html.parser')
#新闻正文页中的标题
print (soup2.select('.main-title')[0].text)
#新闻正文中的时间和来源
#print (soup2.select('.date-source')[0])
#获取的时间格式为字符串
#print (soup2.select('.date-source span')[0].text)
timesource = soup2.select('.date-source')[0].contents[1].text.strip()
#print (timesource)
#print (type(timesource))
#处理时间，字符串转换为时间datetime.strptime,时间转换成字符串datetime.strftime
dt = datetime.strptime(timesource,'%Y年%m月%d日 %H:%M')
print (dt)
#获取新闻正文中的新闻来源
source = soup2.select('.date-source a')[0].text
print (source)
#获取新闻正文内容
#print (soup2.select('.article p'))
#[:-1]去掉列表最后一个元素，编辑信息
#print (soup2.select('.article p')[:-1])
#article = []
#for p in soup2.select('.article p')[:-1]:
    #append给列表新增元素
    #article.append(p.text.strip())
#article中元素中间使用\n换行符连接起来
#'\n'.join(article)
#print (article)
#功能同上，获取新闻正文内容的简写
print ('\n'.join([p.text.strip() for p in soup2.select('.article p')[:-1]]))
#获取责任编辑的信息
editor = soup2.select('.show_author')[0].text.lstrip('责任编辑：')
print (editor)
#获取新闻的评论信息，评论数
comments = requests.get('http://comment5.news.sina.com.cn/page/info?version=1&'
                    'format=json&channel=gn&newsid=comos-fyscrpm0408106&'
                    'group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3&'
                    't_size=3&h_size=3&thread=1')
#print (comments.text.strip('var data='))
jd = json.loads(comments.text.strip('var data='))
print (jd['result']['count']['total'])
#从新闻连接地址中获取评论链接所需的newid
newsurl = 'http://news.sina.com.cn/c/2018-03-10/doc-ifyscrpm0408106.shtml'
newsid = newsurl.split('/')[-1].rstrip('.shtml').lstrip('doc-i')
print (newsid)
#使用正则表达式获取新闻编号
m = re.search('doc-i(.*).shtml',newsurl)
#group(0)会包含要匹配的字符串的全部内容
print (m.group(1))
#获取不同分页的新闻标题和链接
res4 = requests.get('http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page=3&callback=newsloadercallback&_=1520756592631')
jd1 = json.loads(res4.text.lstrip('  newsloadercallback(').rstrip(');'))
for ent in jd1['result']['data']:
    print (ent['url'],ent['title'])