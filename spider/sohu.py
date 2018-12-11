#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: sohu
@time: 18-11-12 下午4:33
"""
import time
import pymongo
from selenium import webdriver
from pyquery import PyQuery as pq

MONGO_URL = 'mongodb://127.0.0.1:27017'
MONGO_DB = 'sina_1'
MONGO_COLLECTION = 'none'

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]

headers = {'Accept': '*/*',
           'Accept-Language': 'zh-CN',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
           'Connection': 'Keep-Alive',
           }

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument("--proxy-server=http://127.0.0.1:1080")
browser = webdriver.Chrome(chrome_options=chrome_options)

URL = 'https://m.weibo.cn/'
MAX = 1500


def get_page(url):

    browser.get(url)
    time.sleep(1)

    buttons = browser.find_elements_by_css_selector('.m-box .nav_item .item_li')

    for i in range(len(buttons)):
        count = MAX
        tag = buttons[i].text
        print('当前tag:', tag)
        if i <= 5:
            continue
        count = min(count, MAX)
        buttons[i].click()
        time.sleep(1)
        for j in range(count):
            print("下拉刷新次数:{}".format(j))
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(0.65)
            html = browser.page_source
            parse_response_sina(html, tag)

        time.sleep(1)


def parse_response_sina(resp, tag):
    doc = pq(resp)
    items = doc('.pannelwrap .wb-item-wrap').items()
    for item in items:
        content = item('.weibo-main').text().replace('\n', '')
        if content and len(content) >= 1:
            user = item('.m-text-box .m-text-cut').eq(0).text()
            compare = content[0:min(len(content), 10)]
            data = {
                'tag': tag,
                'user': user,
                'content': content,
                'compare': compare,
            }
            save_to_mongo(data)
            print(user, content)
    # print(element.text)


def save_to_mongo(data):
    try:
        collection = db[data['tag']]
        # print(data)
        # 采用更新的方式,没有的话会创建,如果url相同则不插入
        collection.update({'compare': data['compare']}, data, upsert=True)
        # collection.insert(data)
    except BaseException as e:
        print("error in save_to_mongo : " + e.__str__())


def main():
    get_page(URL)


if __name__ == '__main__':
    main()

# def parse_response_toutiao(resp):
#     doc = pq(resp)
#     items = doc('.news-list .news-wrapper .news-box').items()
#     for item in items:
#         # print(item.html())
#         try:
#             a = re.search('<h4.*?>(.*?)</h4>', item.html(), re.S).group(1).replace('\n', '')
#             a = pq(a)
#             url = a.attr('href')
#             if url[0] == '/':
#                 url = 'http:' + a.attr('href')
#                 print(url)
#         except BaseException as e:
#             print(e.__str__())
