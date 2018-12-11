#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: test_time
@time: 18-11-7 下午3:50
"""
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import requests
from pyquery import PyQuery as pq

headers = {'Accept': '*/*',
           'Accept-Language': 'zh-CN',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
           'Connection': 'Keep-Alive',
           }
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument("--proxy-server=http://127.0.0.1:1080")
browser = webdriver.Chrome(chrome_options=chrome_options)


# browser = webdriver.Chrome()
def main():
    keyword = '2513'
    page = 2

    url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={0}&k=&num=50&page={1}'.format(keyword, page)
    resp = requests.get(url).content.decode('utf-8')

    j = json.loads(resp, encoding='utf-8')

    data = j['result']['data']

    for v in data:
        # print(v)
        intime = int(v['intime'])
        intime = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(intime)))
        data = {
            'tag': keyword,
            'title': v['title'],
            'url': v['url'],
            'wapurl': v['wapurl'],
            'time': intime,
            'keywords': v['keywords'],
        }
        # print(data)
        get_page(data['wapurl'])


def get_page(url):
    try:
        browser.get(url)
        # print(browser.page_source)
        print(url)
        doc = pq(browser.page_source)
        content = doc('.art_box').text().replace('\n', '')
        print(content)
        # print(url)
        # resp = requests.get(url, headers=headers).content.decode('utf-8', 'ignore')
        # doc = pq(resp)
        # print(doc)
        # content = doc('.art_content').text()
        # content = content.replace('\n', '')
        # print(content)
    except BaseException as e:
        print("error in get_url : " + e.__str__())


if __name__ == '__main__':
    main()
