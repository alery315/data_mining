#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: main_control
@time: 18-12-4 下午2:44
"""
import os
import time

import data_mining.corpus_segment as corpus_segment
import data_mining.save_to_bunch as save_to_bunch
import data_mining.word_vector_space as word_vector_space
import data_mining.chi_square as chi_square
import data_mining.naive_bayes as naive_bayes


def copy_dir():
    if os.path.exists('/home/alery/process/test_corpus_seg_chi'):
        return
    os.system('cp -r /home/alery/process/test_corpus_seg /home/alery/process/test_corpus_seg_chi')
    os.system('cp -r /home/alery/process/train_corpus_seg /home/alery/process/train_corpus_seg_chi')


def process_with_chi_square():
    corpus_segment.main()

    # 将分词结果复制一份用作卡方检验 特征提取
    copy_dir()

    chi_square.main()
    save_to_bunch.main(True)
    word_vector_space.main()
    naive_bayes.main()


def chi_square_after_corpus_seg():
    # 将分词结果复制一份用作卡方检验 特征提取
    copy_dir()

    chi_square.main()
    save_to_bunch.main(True)
    word_vector_space.main()
    naive_bayes.main()


def process_without_chi_square():
    # corpus_segment.main()
    save_to_bunch.main()
    word_vector_space.main()
    naive_bayes.main()


def main():
    start_time = time.time()

    # process_with_chi_square()
    process_without_chi_square()
    # chi_square_after_corpus_seg()

    end_time = time.time()
    print('总耗时：{}秒'.format(int(end_time - start_time)))


if __name__ == '__main__':
    main()