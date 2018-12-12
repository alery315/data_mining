#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: sina
@time: 18-11-6 下午2:06
@desc: 爬取新浪滚动新闻,没有ip限制,没有速度限制
"""
import json
import time
from functools import partial
from multiprocessing.pool import Pool

import pymongo
import requests
from pyquery import PyQuery as pq

# 设置每一类爬取的最大数,会和新浪存在的新闻数量取一个min
number = 105000
count = 0

MONGO_URL = 'mongodb://127.0.0.1:27017'
MONGO_DB = 'sina'

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]


headers = {'Accept': '*/*',
           'Accept-Language': 'zh-CN',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
           'Connection': 'Keep-Alive',
           'Referer': 'https://news.sina.com.cn/roll/',
           }


def get_url(page, keyword):
    try:
        collection = db[keyword]
        print("当前分类为{0},爬取页数为{1}页".format(keyword, page))
        url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={0}&k=&num=50&page={1}'.format(keyword, page)
        resp = requests.get(url).content.decode('utf-8')

        j = json.loads(resp, encoding='utf-8')

        data = j['result']['data']

        for v in data:
            intime = int(v['intime'])
            intime = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(intime)))
            data = {
                'tag': keyword,
                'title': v['title'],
                'url': v['url'],
                'time': intime,
                'keywords': v['keywords'],
            }
            # print(data)
            get_page(data, v['url'], collection=collection)
        return j['result']['total']
    except BaseException as e:
        print("error in get_url : " + e.__str__())


def get_page(data, url, collection):
    try:
        resp = requests.get(url).content.decode('utf-8', 'ignore')
        doc = pq(resp)
        content = doc('.article').text()
        # print(url)
        if not content:
            content = doc('#artibody').text()
        content = content.replace('\n', '')
        data['content'] = content
        save_to_mongo(data, collection)
    except BaseException as e:
        print("error in get_url : " + e.__str__())


def save_to_mongo(data, collection):
    try:
        # print(data)
        # 采用更新的方式,没有的话会创建,如果url相同则不插入
        # collection.update({'url': data['url']}, data, upsert=True)
        collection.insert(data)
    except BaseException as e:
        print("error in get_url : " + e.__str__())


def main(keyword):
    # get_page()
    total = get_url(1, keyword=keyword)
    print("---------当前分类下共{}条新闻.---------".format(total))
    total = min(number, total)
    page = int(total / 50)
    # page = 3
    pool = Pool()
    pool.map(partial(get_url, keyword=keyword), [i for i in range(2, page)])
    pool.close()
    pool.join()


if __name__ == '__main__':
    tags = [str(i) for i in range(2510, 2519)]
    print(tags)
    for v in tags:
        main(v)
