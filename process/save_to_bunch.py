#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: save_to_bunch
@time: 18-11-26 下午2:50
"""
import os
import _pickle as pickle
import time
from data_mining.config import *
import threadpool
from sklearn.datasets.base import Bunch


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def corpus_to_bunch(word_bag_path, seg_path):
    cate_list = os.listdir(seg_path)

    bunch = Bunch(target_name=[], label=[], filenames=[], contents=[])
    bunch.target_name.extend(cate_list)

    for mydir in cate_list:
        class_path = seg_path + mydir + "/"
        file_list = os.listdir(class_path)

        def to_bunch(path):
            bunch.label.append(mydir)
            bunch.filenames.append(path)
            bunch.contents.append(read_file(path))

        # 多进程
        # pool = Pool()
        # # partial_work = partial(split_word_by_cate, corpus_path=corpus_path, seg_path=seg_path)
        # pool.map(to_bunch, [class_path + file for file in file_list])
        # pool.close()
        # pool.join()

        # 多线程
        pool = threadpool.ThreadPool(THREAD_NUM)
        requests = threadpool.makeRequests(to_bunch, [class_path + file for file in file_list][:TEST_NUM])
        [pool.putRequest(req) for req in requests]
        pool.wait()

        # for file in file_list:
        #     file_name = class_path + file  # 文件全名
        #     bunch.label.append(mydir)
        #     bunch.filenames.append(file_name)
        #     bunch.contents.append(read_file(file_name))
        print(mydir, '类 bunch对象插入完成!')
    with open(word_bag_path, 'wb') as f:
        pickle.dump(bunch, f)

    print('构建文本对象结束')


def main():
    start_time = time.time()

    corpus_to_bunch(train_bunch_path, train_corpus_seg_path)
    corpus_to_bunch(test_bunch_path, test_corpus_seg_path)

    end_time = time.time()
    print('保存到bunch耗时：{}秒'.format(int(end_time - start_time)))


if __name__ == '__main__':
    main()
