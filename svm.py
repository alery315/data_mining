#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: svm
@time: 18-12-11 下午7:48
"""
import pickle

from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.svm import SVC
from sklearn import metrics


def read_bunch_obj(file):
    with open(file, 'rb') as f:
        bunch = pickle.load(f)
    return bunch


# 计算分类精度：
def metrics_result(actual, predict):
    print('正确率:{0:.3f}'.format(metrics.precision_score(actual, predict, average='weighted')))
    print('召回率:{0:0.3f}'.format(metrics.recall_score(actual, predict, average='weighted')))
    print('f1-score:{0:.3f}'.format(metrics.f1_score(actual, predict, average='weighted')))


def main():
    base_path = '/home/alery/process/'
    # 导入训练集
    train_path = base_path + "train_word_bag/tfidf_space.dat"
    train_set = read_bunch_obj(train_path)

    # 导入测试集
    test_path = base_path + "test_word_bag/test_space.dat"
    test_set = read_bunch_obj(test_path)

    print('train词向量矩阵shape: ', train_set.tdm.shape)
    print('test词向量矩阵shape: ', test_set.tdm.shape)

    svc_cl = SVC(gamma='auto')
    pipe = make_pipeline(train_set.vec[0], svc_cl)
    pipe.fit(train_set.contents, train_set.label)
    pred = pipe.predict(test_set.contents)
    metrics_result(test_set.label, pred)


if __name__ == '__main__':
    main()
