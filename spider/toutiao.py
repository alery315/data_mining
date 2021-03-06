#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: test
@time: 18-11-6 下午4:00
@desc: 爬取头条新闻分类,但是容易被封ip,需要加大sleep参数,其中有个加密的参数,需要单独用decode.js解密(别人写的). 这个爬虫容易被封,爬到的数据不多
"""
from multiprocessing.pool import Pool

import pymongo
import requests
import re
import json
import random
from pyquery import PyQuery as pq
import hashlib
import execjs
import time
import pandas as pd

requests.packages.urllib3.disable_warnings()  # 禁止提醒SSL警告

BASE_URL = 'http://www.toutiao.com/'
KEYWORD = 'news_military'
NUMBER = 15000
TIME_SLEEP = 0.1

MONGO_URL = 'mongodb://127.0.0.1:27017'
MONGO_DB = 'toutiao'
MONGO_COLLECTION = KEYWORD

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]
headers = {'Accept': '*/*',
           'Accept-Language': 'zh-CN',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
           'Connection': 'Keep-Alive',
           }


class Toutiao(object):

    def __init__(self, keyword):
        self.url = BASE_URL + 'ch/' + keyword
        self.s = requests.session()
        self.s.headers.update(headers)
        self.keyword = keyword

    def closes(self):
        self.s.close()
        client.close()

    def getdata(self):  # 获取数据

        req = self.s.get(url=self.url, verify=False)
        # print (self.s.headers)
        # print(req.text)
        headers = {'referer': self.url}
        max_behot_time = '0'
        signature = '.1.hXgAApDNVcKHe5jmqy.9f4U'
        eas = 'A1E56B6786B47FE'
        ecp = '5B7674A7FF2E9E1'
        self.s.headers.update(headers)

        for i in range(0, NUMBER):  # 获取页数
            try:
                Honey = json.loads(self.get_js())
                eas = Honey['as']
                ecp = Honey['cp']
                signature = Honey['_signature']
                url = 'http://www.toutiao.com/api/pc/feed/?category={}&utm_source=toutiao&widen=1&max_behot_time={}&max_behot_time_tmp={}&tadrequire=true&as={}&cp={}&_signature={}'.format(
                    self.keyword, max_behot_time, max_behot_time, eas, ecp, signature)
                req = self.s.get(url=url, verify=False)
                # print(req.text)
                # print(url)
                j = json.loads(req.text)
                # max_behot_time = j['next']['max_behot_time']
                pool = Pool()
                pool.map(self.get_news, [v for v in j['data']])
                pool.close()
                pool.join()
                print('------------' + str(j['next']['max_behot_time']))
            except BaseException as e:
                print("error in get_data: " + e.__str__())

    def get_news(self, j):
        # article_genre: "gallery" 这个是图片集没有文字
        # tag: "ad" 这个是广告
        try:
            if j['tag'] != 'ad' and j['article_genre'] != 'gallery' \
                    and j['tag'] != 'forum_post':
                title = j['title']  # 标题
                source_url = BASE_URL + j['source_url']  # 文章链接
                tag = j['tag']  # 频道名
                try:
                    chinese_tag = (j['chinese_tag'])  # 频道中文名
                except:
                    chinese_tag = ''
                try:
                    if j['label']:
                        label = [j['label']]  # 标签
                except:
                    label = []
                behot = int(j['behot_time'])
                behot_time = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(behot)))  # 发布时间
                data = {'title': title, 'url': source_url,
                        'tag': tag,
                        'chinese_tag': chinese_tag, 'label': label,
                        'time': behot_time,
                        }

                # 获取网页内容
                data['content'] = self.get_content(data['url'])

                # 保存到mongodb
                collection.insert(data)
                time.sleep(TIME_SLEEP)

                # 保存到csv
                self.save_url_to_csv(data)

        except BaseException as e:
            # print(data['url'])
            print("error in get_news: " + e.__str__())
        # time.sleep(0.5)

    # 保存url到csv
    def save_url_to_csv(self, data):
        df = pd.DataFrame(data=data)
        df.to_csv(r'toutiao.csv', mode='a', encoding='UTF-8', header=False, index=False)

    # 获取新闻内容
    def get_content(self, url):
        resp = requests.get(url, headers=headers, verify=False)
        html = pq(resp.content.decode('utf-8'))
        # print(html.html())
        content = re.search("content: '(.*?)',", html.html(), re.S).group(1)
        content = content.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
        html = pq(content).text()
        # print(html)
        return html

    def getHoney(self, t):  # 根据JS脚本破解as ,cp
        e = str('%X' % t)  # 格式化时间
        m1 = hashlib.md5()  # MD5加密
        m1.update(str(t).encode(encoding='utf-8'))  # 转化格式
        i = str(m1.hexdigest()).upper()  # 转化大写
        # print(i)
        n = i[0:5]  # 获取前5位
        a = i[-5:]  # 获取后5位
        s = ''
        r = ''
        for x in range(0, 5):
            s += n[x] + e[x]
            r += e[x + 3] + a[x]
        eas = 'A1' + s + e[-3:]
        ecp = e[0:3] + r + 'E1'
        # print(eas)
        # print(ecp)
        return eas, ecp

    def get_js(self):
        f = open(r"decode.js", 'r', encoding='UTF-8')
        line = f.readline()
        htmlstr = ''
        while line:
            htmlstr = htmlstr + line
            line = f.readline()
        ctx = execjs.compile(htmlstr)
        return ctx.call('get_as_cp_signature')


if __name__ == '__main__':
    t = Toutiao(KEYWORD)
    t.getdata()
    t.closes()
