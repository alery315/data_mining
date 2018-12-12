#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: word_vector_space
@time: 18-11-26 下午3:17
"""
import _pickle as pickle
import time

from sklearn.datasets.base import Bunch
from sklearn.feature_extraction.text import TfidfVectorizer
from data_mining.config import *


def read_file(file):
    with open(file, 'r') as f:
        return f.read()


def read_bunch_obj(file):
    with open(file, 'rb') as f:
        bunch = pickle.load(f)
    return bunch


def write_bunch_obj(path, bunch):
    with open(path, 'wb') as file:
        pickle.dump(bunch, file)


def tf_idf(stop_word_file, bunch_path, space_path, train_tfidf_path=None):
    stop_word_list = read_file(stop_word_file).replace('\n', ' ').split()
    bunch = read_bunch_obj(bunch_path)

    tfidf_space = Bunch(target_name=bunch.target_name,
                        label=bunch.label,
                        filenames=bunch.filenames,
                        tdm=[],
                        vocabulary=[],
                        vec=None)

    '''
    sublinear_tf 计算tf采用亚线性策略,以前是词频,现在用1+log(tf)来当词频
    max_df 文档频率过高,作为临时停用词
    min_df 文档频率太低,增加了维度,可以适当控制
    '''
    if train_tfidf_path is not None:
        trainbunch = read_bunch_obj(train_tfidf_path)
        tfidf_space.vocabulary = trainbunch.vocabulary
        vectorizer = TfidfVectorizer(stop_words=stop_word_list, sublinear_tf=True, max_df=0.35, min_df=0.0005,
                                     vocabulary=trainbunch.vocabulary)
        tfidf_space.vec = vectorizer
        tfidf_space.tdm = vectorizer.fit_transform(bunch.contents)
    else:
        vectorizer = TfidfVectorizer(stop_words=stop_word_list, sublinear_tf=True, max_df=0.35, min_df=0.0005)
        tfidf_space.vec = vectorizer
        tfidf_space.tdm = vectorizer.fit_transform(bunch.contents)
        tfidf_space.vocabulary = vectorizer.vocabulary_

    write_bunch_obj(space_path, tfidf_space)
    print('tf-idf词向量创建成功')


def main():
    start_time = time.time()

    tf_idf(stop_word_path, train_bunch_path, train_space_path)

    tf_idf(stop_word_path, test_bunch_path, test_space_path, train_space_path)

    end_time = time.time()
    print('tf_idf耗时：{}秒'.format(int(end_time - start_time)))


if __name__ == '__main__':
    main()
