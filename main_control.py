#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: main_control
@time: 18-12-4 下午2:44
@desc: 这个入口写的不太好,主要中间有很多参数需要弄,还是单独调好每个文件的参数再来运行这个
"""
import multiprocessing
import os
import time
from functools import partial
from multiprocessing.pool import Pool

import data_mining.process.corpus_segment as corpus_segment
import data_mining.process.save_to_bunch as save_to_bunch
import data_mining.process.word_vector_space as word_vector_space
import data_mining.process.chi_square as chi_square
import data_mining.process.naive_bayes as naive_bayes


def process_with_chi_square():
    corpus_segment.main()
    chi_square.main()
    save_to_bunch.main()
    word_vector_space.main()
    naive_bayes.main()


def chi_square_after_corpus_seg():
    chi_square.main()
    save_to_bunch.main()
    word_vector_space.main()
    naive_bayes.main()


def process_without_chi_square():
    # corpus_segment.main()
    save_to_bunch.main()
    word_vector_space.main()
    naive_bayes.main()


def test(i, x):
    print(i, 5)


def worker(name, que):
    que.put("%d is done" % name)


def work(n, a, num):
    print('%s run' % os.getpid())
    time.sleep(3)
    print(a)
    num[a] += 1
    return n ** 2


def adddata(datalist):
    datalist.append(1)
    datalist.append(2)
    datalist.append(3)
    print("子进程", os.getpid(), datalist)


def main():
    start_time = time.time()

    # process_with_chi_square()
    # process_without_chi_square()
    # chi_square_after_corpus_seg()

    # pool = Pool(10)
    # partial_work = partial(test, x=5)
    # pool.map(partial_work, [i for i in range(1)])
    # pool.close()
    # pool.join()
    datalist = multiprocessing.Manager().list(range(10))
    p = multiprocessing.Process(target=adddata, args=(datalist,))
    p.start()
    p.join()
    datalist.append("a")
    datalist.append("b")
    datalist.append("c")
    print("主进程", os.getpid(), datalist)

    end_time = time.time()
    print('总耗时：{}秒'.format(int(end_time - start_time)))


if __name__ == '__main__':
    main()
