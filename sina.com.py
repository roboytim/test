import requests
from bs4 import  BeautifulSoup
res = requests.get('http://news.sina.com.cn/china/')
#输出响应码200
print (res)
#输出res的默认编码格式
print (res.encoding)
#更改res的编码方式为UTF-8
res.encoding = 'utf-8'
#输出文本内容
print (res.text)