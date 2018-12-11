#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: sohu
@time: 18-11-12 下午4:33
"""
import os

import pandas as pd
import time
import re
import pymongo
from selenium import webdriver
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# ---------------------------------------配置信息-----------------------------------

KEYWORD = '汽车'

MONGO_URL = 'mongodb://127.0.0.1:27017'
MONGO_DB = 'baidu'
MONGO_COLLECTION = 'auto'

SLEEP_TIME = 0.5  # 经常崩的话调大这个

PATH = 'data'  # 保存数据的路径,目前表示在当前文件夹下创建data文件夹保存

URL = 'https://www.baidu.com/'

# ---------------------------------------配置信息-----------------------------------

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

headers = {'Accept': '*/*',
           'Accept-Language': 'zh-CN',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
           'Connection': 'Keep-Alive',
           }

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')  # 这种页面需要来回点击,还是不要开无头模式了
# chrome_options.add_argument("--proxy-server=http://127.0.0.1:1080")  #代理
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.maximize_window()


def get_page(url):
    browser.get(url)
    time.sleep(0.5)

    kw = browser.find_element_by_id('kw')
    kw.send_keys(KEYWORD)

    su = browser.find_element_by_id('su')
    su.click()

    time.sleep(0.5)

    tab = browser.find_elements_by_css_selector('#s_tab .s_tab_inner > a')[0]
    tab.click()

    time.sleep(0.5)

    for i in range(1000):
        next_button = browser.find_elements_by_css_selector('#page > a')[-1]
        next_button.click()
        time.sleep(0.05)

    # button = browser.find_elements_by_css_selector('.detail .tab-main > ul > li')[4]  # 定位button
    # button.click()
    # browser.execute_script('arguments[0].scrollIntoView(true);', button)  # 滑动到评论处
    #
    # wait = WebDriverWait(browser, 10)
    # wait.until(EC.presence_of_element_located((By.ID, 'comment')))  # 等待数据加载
    #
    # time.sleep(3)  # 还是
    # comments = browser.find_elements_by_css_selector('#comment .mc .comments-list .filter-list > li a')


# 保存url到csv
def save_url_to_csv(data, cate):
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    df = pd.DataFrame(data=data, index=[0])
    # if os.path.exists('data/' + cate + '.csv'):
    #     with open('test.txt', mode='a', encoding='utf-8') as f:
    #         f.read()
    df.to_csv(PATH + '/' + cate + '.csv', mode='a', encoding='UTF-8', header=False, index=False)


def save_to_mongo(data):
    try:
        # print(data)
        # 采用更新的方式,没有的话会创建,如果url相同则不插入
        # collection.update({'compare': data['compare']}, data, upsert=True)
        collection.insert(data)
    except BaseException as e:
        print("error in save_to_mongo : " + e.__str__())


def all_dirs(path):
    for root, dirs, files in os.walk(path):
        return dirs


def all_files(path):
    for root, dirs, files in os.walk(path):
        return files


def count_data():
    count = 0
    files = all_files(PATH)
    for file in files:
        file = PATH + '/' + file
        with open(file, 'r', encoding='utf-8') as f:
            s = f.read().split('\n')
            print(file, len(s))
            count += len(s)

    print("---------目前一共有{}条数据----------".format(count))


def main():
    start = time.time()

    get_page(url=URL)

    # browser.close()
    end = time.time()
    print('程序运行时间为:%.2f秒' % (end - start))


if __name__ == '__main__':
    main()
