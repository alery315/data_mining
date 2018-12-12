#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: split_file
@time: 18-11-15 下午5:05
"""
import os
import time
from pyquery import PyQuery as pq

import requests

START = 1
BASE_PATH = '/home/alery/split/'
SPLIT_COUNT = 5000


def all_dirs(path):
    for root, dirs, files in os.walk(path):
        return dirs


def all_files(path):
    for root, dirs, files in os.walk(path):
        return files


def make_sub_file(lines, head, src_name, sub):
    [des_filename, ext_name] = os.path.splitext(src_name)
    file = des_filename[des_filename.rfind('/') + 1:]
    # print(file)
    filename = des_filename + '/' + file + '_' + str(sub) + ext_name
    if not os.path.exists(des_filename):
        os.mkdir(des_filename)
    print('make file: %s' % filename)
    fout = open(filename, 'w')
    try:
        # fout.writelines([head])
        fout.writelines(lines)
        return sub + 1
    finally:
        fout.close()


def split_by_line_count(filename, count):
    fin = open(filename, 'r')
    try:
        head = fin.readline()
        buf = []
        sub = START
        for line in fin:
            buf.append(line)
            if len(buf) == count:
                sub = make_sub_file(buf, head, filename, sub)
                buf = []
        if len(buf) != 0:
            make_sub_file(buf, head, filename, sub)
    finally:
        fin.close()


# 统计一共有多少数据
def count_data():
    base_path = '/home/alery/sina/count/'
    dirs = all_dirs(base_path)
    sum_all = 0
    for d in dirs:
        count = 0
        files = all_files(base_path + d)
        for file in files:
            file = base_path + d + '/' + file
            with open(file, 'r', encoding='utf-8') as f:
                s = f.read().split('\n')
                # print(file, len(s))

                # 按每行字符大于65计算数目
                for v in s:
                    if len(v) >= 65:
                        count += 1

                # 直接按行数计算
                # count += len(s)
        sum_all += count
        print("--------- {0} 一共有:{1}条数据----------".format(d, count))
    print("---------一共有 {} 条数据----------".format(sum_all))


def split_file(l):
    for i in l:
        split_by_line_count(BASE_PATH + i, SPLIT_COUNT)


def get_page(url):
    try:
        resp = requests.get(url).content.decode('utf-8', 'ignore')
        doc = pq(resp)
        content = doc('.article').text()

        content = content.replace('\n', '')
        # print(url)
        print(content)
    except BaseException as e:
        print("error in get_url : " + e.__str__())


def cate_data(file):
    with open(file, 'r', encoding='utf-8') as f:
        count = 0
        for line in f:
            # if count == 1000:
            #     break
            count += 1
            data = line.split('|,|', 2)
            try:
                cate = data[1]
                content = data[2]
                # print(cate)
                if cate and content:
                    idx1 = cate.find('news_')
                    if idx1 != -1:
                        idx2 = len(cate) if cate.find('/', idx1) == -1 else cate.find('/', idx1)
                        cate = cate[idx1:idx2]
                        if cate.find(',') != -1:
                            cate = cate[:cate.find(',')]
                    else:
                        continue
                    content = content.replace('|,|', '')
                    # print(count1)
                    # print(cate, content)
                    write_to_csv(cate, content)
            except IndexError as e:
                # print('list index out of range')
                pass
        print(count)


def write_to_csv(cate, content):
    file = cate + '.csv'
    with open(BASE_PATH + file, 'a+', encoding='utf-8') as f:
        f.write(content)


def main():
    begin = time.time()

    files = all_files(BASE_PATH)
    print(files)
    split_file(files)

    # # 分类数据
    # for file in files:
    #     cate_data(BASE_PATH + file)

    # 计算数据数量
    # count_data()

    end = time.time()
    print('time is %d seconds ' % (end - begin))


if __name__ == '__main__':
    main()
