#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: word_vector_space
@time: 18-11-26 下午3:17
"""
import _pickle as pickle
from sklearn.datasets.base import Bunch
from sklearn.feature_extraction.text import TfidfVectorizer


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
                        contents=bunch.contents,
                        tdm=[],
                        vocabulary=[],
                        vec=[])

    '''
    sublinear_tf 计算tf采用亚线性策略,以前是词频,现在用1+log(tf)来当词频
    max_df 文档频率过高,作为临时停用词
    min_df 文档频率太低,增加了维度,可以适当控制
    '''
    if train_tfidf_path is not None:
        trainbunch = read_bunch_obj(train_tfidf_path)
        tfidf_space.vocabulary = trainbunch.vocabulary
        vectorizer = TfidfVectorizer(stop_words=stop_word_list, sublinear_tf=True, max_df=0.35, min_df=0.001,
                                     vocabulary=trainbunch.vocabulary)
        tfidf_space.vec = [vectorizer]
        tfidf_space.tdm = vectorizer.fit_transform(bunch.contents)
    else:
        vectorizer = TfidfVectorizer(stop_words=stop_word_list, sublinear_tf=True, max_df=0.35, min_df=0.001)
        tfidf_space.vec = [vectorizer]
        tfidf_space.tdm = vectorizer.fit_transform(bunch.contents)
        tfidf_space.vocabulary = vectorizer.vocabulary_

    write_bunch_obj(space_path, tfidf_space)
    print('tf-idf词向量创建成功')


def main():
    base_path = '/home/alery/process/'
    stop_word = 'stopwords.txt'
    bunch_path = base_path + 'train_word_bag/train_set.dat'
    space_path = base_path + 'train_word_bag/tfidf_space.dat'
    tf_idf(stop_word, bunch_path, space_path)

    bunch_path = base_path + "test_word_bag/test_set.dat"
    space_path = base_path + "test_word_bag/test_space.dat"
    train_tfidf_path = base_path + "train_word_bag/tfidf_space.dat"
    tf_idf(stop_word, bunch_path, space_path, train_tfidf_path)


if __name__ == '__main__':
    main()
