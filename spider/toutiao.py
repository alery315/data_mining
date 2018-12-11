#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: test
@time: 18-11-6 下午4:00
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
from data_mining.new import News


requests.packages.urllib3.disable_warnings()  # 禁止提醒SSL警告


BASE_URL = 'https://www.toutiao.com/'
KEYWORD = 'news_military'
NUMBER = 12000

MONGO_URL = 'mongodb://127.0.0.1:27017'
MONGO_DB = 'toutiao'
MONGO_COLLECTION = KEYWORD

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]


class Toutiao(object):

    def __init__(self, keyword):
        self.url = BASE_URL + 'ch/' + keyword
        self.s = requests.session()
        headers = {'Accept': '*/*',
                   'Accept-Language': 'zh-CN',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
                   'Connection': 'Keep-Alive',

                   }
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

        for i in range(0, NUMBER):  ##获取页数

            Honey = json.loads(self.get_js())
            eas = Honey['as']
            ecp = Honey['cp']
            signature = Honey['_signature']
            url = 'https://www.toutiao.com/api/pc/feed/?category={}&utm_source=toutiao&widen=1&max_behot_time={}&max_behot_time_tmp={}&tadrequire=true&as={}&cp={}&_signature={}'.format(
                self.keyword, max_behot_time, max_behot_time, eas, ecp, signature)
            req = self.s.get(url=url, verify=False)
            print(req.text)
            print(url)
            j = json.loads(req.text)
            # max_behot_time = j['next']['max_behot_time']
            for k in range(0, len(j['data'])):
                # article_genre: "gallery" 这个是图片集没有文字
                # tag: "ad" 这个是广告
                try:
                    if j['data'][k]['tag'] != 'ad' and j['data'][k]['article_genre'] != 'gallery' \
                            and j['data'][k]['tag'] != 'forum_post':
                        title = (j['data'][k]['title'])  # 标题
                        source_url = ('https://www.toutiao.com/' + j['data'][k]['source_url'])  # 文章链接
                        tag = (j['data'][k]['tag'])  # 频道名
                        # try:
                        #     chinese_tag = (j['data'][k]['chinese_tag'])  # 频道中文名
                        # except:
                        #     chinese_tag = ''
                        try:
                            if j['data'][k]['label']:
                                label = (j['data'][k]['label'])  # 标签
                        except:
                            label = []
                        behot = int(j['data'][k]['behot_time'])
                        behot_time = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(behot)))  # 发布时间
                        data = {'title': title, 'url': source_url,
                                'tag': tag,
                                'label': label,
                                'time': behot_time,
                                }

                        data['content'] = self.get_content(data['url'])
                        collection.insert(data)
                except BaseException as e:
                    # print(data['url'])
                    print("error : " + e.__str__())
            time.sleep(0.2)
            print('------------' + str(j['next']['max_behot_time']))
            # 保存到csv
            # df = pd.DataFrame(data=data)
            # df.to_csv(r'toutiao.csv', encoding='UTF-8', index=0)

    # 获取新闻内容
    def get_content(self, url):
        resp = self.s.get(url, verify=False)
        html = pq(resp.content.decode('utf-8'))
        content = re.search("content: '(.*?)',", html.html(), re.S).group(1)
        content = content.replace('lt;', '<').replace('gt;', '>').replace('&amp;', '').replace('&quot;', '"')
        html = pq(content).text()
        time.sleep(0.1)
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
