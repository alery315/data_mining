#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: content
@time: 18-11-6 下午8:28
"""
import re
import html
import requests
from pyquery import PyQuery as pq
from html.parser import HTMLParser

# 120.198.224.104:8080#中国 广东 汕头
# 120.198.224.110:8000#中国 广东 汕头
# 120.198.224.102:8080#中国 广东 汕头
# 114.242.25.152:3128#中国 北京 北京
# 120.198.224.109:8080#中国 广东 汕头

proxies = {
    'http': 'http://60.191.134.165:9999',
    'https': 'https://60.191.134.165:9999'
}


def main():
    url = 'https://www.toutiao.com/a6619966781165404676/'
    # url = 'https://ip.cn/'
    headers = {'Accept': '*/*',
               'Accept-Language': 'zh-CN',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
               }
    resp = requests.get(url, headers=headers, proxies=proxies)
    htm = pq(resp.content.decode('utf-8'))
    print(htm)
    content = re.search("content: '(.*?)',", htm.html(), re.S).group(1)
    content = content.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
    htm = pq(content)
    print(htm.text())



if __name__ == '__main__':
    for i in range(100):
        main()
