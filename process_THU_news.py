#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: test_threadpool
@time: 18-11-30 下午1:33
"""
import os
import time

import threadpool

storage = []


def say_hello(s):
    storage.append(s)
    print("Hello ", s)
    time.sleep(3)


def test_thread():
    print(storage)
    name_list = ['xiaozi', 'aa', 'bb', 'cc', 'xiaozi', 'aa', 'bb', 'cc', 'xiaozi', 'aa', 'bb', 'cc',
                 'xiaozi', 'aa', 'bb', 'cc', 'xiaozi', 'aa', 'bb', 'cc', 'xiaozi', 'aa', 'bb', 'cc']
    start_time = time.time()
    pool = threadpool.ThreadPool(32)
    requests = threadpool.makeRequests(say_hello, name_list)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    print(storage)
    print('%d second' % (time.time() - start_time))


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().replace('\n', '')


def write_file(path, content):
    with open(path, 'a+', encoding='utf-8') as f:
        f.write(content + '\n')


def main():
    path = '/home/alery/下载/THUCNews/THUCNews/游戏'
    files = os.listdir(path)
    print(len(files))
    count = 0
    for file in files:
        file_path = os.path.join(path, file)
        write_file('/home/alery/process/game_{}.csv'.format(int(count / 5000)), read_file(file_path))
        # print(read_file(file_path))
        count += 1


if __name__ == '__main__':
    main()
