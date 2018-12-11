#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: split.py
@time: 2018/11/11 21:37
"""

import collections
import os
import re
from multiprocessing.pool import Pool

import pymongo

MONGO_URL = 'mongodb://127.0.0.1:27017'
MONGO_DB = 'sohu'
MONGO_COLLECTION = 'none'

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]

collections_test = ['news', 'yule', 'mil', 'auto', 'caipiao', 'sports', 'business', 'cul']


def all_dirs(path):
    for root, dirs, files in os.walk(path):
        return dirs


def all_files(path):
    for root, dirs, files in os.walk(path):
        return files


def process_content(path):
    print(path)
    cates = []
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        arr = s.split('http:')
        for v in arr:
            try:
                cate = re.search("//(.*?)\.sohu\.com", v[0:100], re.S).group(1)
                idx = cate.find('.')
                cate = cate[idx + 1:]
                # cate = v[0: v.find('.sohu.com/')]
                cates.append(cate)
                v = v[v.find('`1`2') + 4:]
                v = v.replace('\n', '').replace('`1`2', '').replace('本报记者', '').replace('实习记者', '')
                if cate in collections_test:
                    data = {
                        'tag': cate,
                        'content': v,
                    }
                    save_to_mongo(data)
            except AttributeError as e:
                pass
                # print(e.__str__())
        # print(len(arr))

    # items = collections.Counter(cates)
    #
    # for k, v in items.items():
    #     if v < 10:  # 反正这个数也比较小
    #         for i in range(v):
    #             cates.remove(k)
    # print(items)
    # return set(cates)


def save_to_mongo(data):
    try:
        collection = db[data['tag']]
        # print(data)
        # 采用更新的方式,没有的话会创建,如果url相同则不插入
        # collection.update({'content': data['content']}, data, upsert=True)
        collection.insert(data)
    except BaseException as e:
        print("error in save_to_mongo : " + e.__str__())


def main():

    base_path = '/home/alery/文档/sohu'

    dirs = all_dirs(base_path)

    # s = set()

    for d in dirs:
        d = base_path + '/' + d
        files = all_files(d)
        pool = Pool()
        pool.map(process_content, [d + '/' + file for file in files])
        pool.close()
        pool.join()
        # for file in files:
        #     file = d + '/' + file
        #     process_content(file)
        # for i in range(30):
        #     file = d + '/' + files[i]
        #
        #     s = s | process_content(file)

    # print(s)


class Main:
    def __init__(self):
        pass


if __name__ == '__main__':
    main()
