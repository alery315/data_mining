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

MONGO_URL = 'mongodb://127.0.0.1:27017'
MONGO_DB = 'jingdong'
MONGO_COLLECTION = 'comment'

SLEEP_TIME = 0.5  # 经常崩的话调大这个

PATH = 'data'  # 保存数据的路径,目前表示在当前文件夹下创建data文件夹保存

# 前面是商品url,后面是名字,也就是保存csv的文件名
# 这个url也可以自己按关键词爬..
URLS = {
    'https://item.jd.com/7435156.html': '惠普暗影4',
    'https://item.jd.com/7652159.html': ' 小米8',
    'https://item.jd.com/7652161.html': '小米8 se',
    'https://item.jd.com/100000203560.html': '荣耀8x',
    'https://item.jd.com/7081550.html': '荣耀10',
}

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
    time.sleep(1)

    button = browser.find_elements_by_css_selector('.detail .tab-main > ul > li')[4]  # 定位button
    button.click()
    browser.execute_script('arguments[0].scrollIntoView(true);', button)  # 滑动到评论处

    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'comment')))  # 等待数据加载

    time.sleep(3)  # 还是
    comments = browser.find_elements_by_css_selector('#comment .mc .comments-list .filter-list > li a')

    # 2 - 5 分别表示 差评 中评 好评 追评, 从li的列表倒着数
    for i in range(2, 6):
        comment = comments[-i]
        # 定位到评论处,防止点击错误,但是有时候还是会发生- -
        browser.execute_script('arguments[0].scrollIntoView(true);', button)
        time.sleep(0.3)
        comment.click()
        page = re.search('\((.*?)\+\)', comment.text, re.S).group(1)
        if page.find('万') != -1:
            page = 1000
        page = int(int(page) / 10)
        print('-' * 40 + str(page) + '-' * 40)
        page = min(99, page)
        time.sleep(3)
        for j in range(page - 2):  # 防止到最后一页没有了下一页按钮
            try:
                doc = pq(browser.page_source)
                items = doc('#comment .mc .comments-list .tab-con #comment-' + str(8 - i) + ' .comment-item').items()
                flag = False  # 定义一个标记,表示本页是否有数据
                for item in items:
                    # print(item)
                    flag = True
                    content = item('.comment-con').text().replace('\n', '')
                    print(content)
                    data = {
                        'tag': str(i),
                        'content': content,
                    }
                    # collection.insert(data)
                    save_url_to_csv(data=data, cate=URLS[url])

                # 有时候会没有数据,但是页数还是可以点击下一页,这种情况直接break
                if not flag:
                    break

                # 这句重灾区,经常定位不到,加大延时,过快导致下一页按钮没加载出来
                next_page = browser.find_element_by_css_selector('#comment .mc .comments-list .tab-con #comment-'
                                                                 + str(8 - i) + ' .ui-page > a.ui-pager-next')
                # print(next_page.text)
                # browser.execute_script('arguments[0].scrollIntoView(true);', next_page)
                next_page.click()
                time.sleep(0.35)
            except BaseException as e:
                print(e.__str__())
                break


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


def main():
    start = time.time()

    try:
        for k, v in URLS.items():
            print(k, v)
            get_page(k)
    except BaseException as e:
        print(e.__str__())

    browser.close()

    count = 0
    files = all_files(PATH)
    for file in files:
        file = PATH + '/' + file
        with open(file, 'r', encoding='utf-8') as f:
            s = f.read().split('\n')
            print(file, len(s))
            count += len(s)

    print("---------目前一共有{}条数据----------".format(count))

    end = time.time()
    print('程序运行时间为:%.2f秒' % (end - start))


if __name__ == '__main__':
    main()
