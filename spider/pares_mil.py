#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: pares_mil
@time: 18-11-12 下午8:17
"""
import re
import time

import pymongo
import requests
from pyquery import PyQuery as pq

headers = {'Accept': '*/*',
           'Accept-Language': 'zh-CN',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
           }
MONGO_URL = 'mongodb://127.0.0.1:27017'
MONGO_DB = 'toutiao'
MONGO_COLLECTION = 'news_military'

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]


def get_content(url):
    try:
        resp = requests.get(url, headers=headers).content.decode('utf-8')
        # print(resp)
        content = re.search("content: '(.*?)',", resp, re.S).group(1)
        content = content.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
        html = pq(content).html().replace('\n', '')
        data = {
            'tag': MONGO_COLLECTION,
            'content': html,
        }
        collection.insert(data)
    except BaseException as e:
        print(e.__str__())


def main():
    base_url = 'https://www.toutiao.com'
    with open('mil.html', 'r', encoding='utf-8') as f:
        html = pq(f.read())
        items = html('.index-content .feedBox .wcommonFeed > ul > li').items()
        for item in items:
            a = item('.title-box a')
            if a and a.attr('href')[0] == '/':
                url = base_url + a.attr('href')
                title = a.text()
                print(url, title)
                get_content(url)
                time.sleep(0.2)

    pass


if __name__ == '__main__':
    main()
