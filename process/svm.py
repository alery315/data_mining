#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: svm
@time: 18-12-11 下午7:48
"""
import pickle
import time

from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from data_mining.process.manual_naive_bayes import *


def read_bunch_obj(file):
    with open(file, 'rb') as f:
        bunch = pickle.load(f)
    return bunch


def read_result(path):
    M = np.zeros([10, 10])
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            label, excepted_label = line.strip().split(' ')
            # print(label, excepted_label)
            M[label_dict[label], label_dict[excepted_label]] += 1
    return M


# 计算分类精度：
def metrics_result(actual, predicted):
    print('正确率:{0:.3f}'.format(metrics.precision_score(actual, predicted, average='weighted')))
    print('召回率:{0:0.3f}'.format(metrics.recall_score(actual, predicted, average='weighted')))
    print('f1-score:{0:.3f}'.format(metrics.f1_score(actual, predicted, average='weighted')))


def main():
    # 设置混淆矩阵不用科学计数法输出
    np.set_printoptions(suppress=True)

    start = time.time()

    # # 导入训练集
    # train_set = read_bunch_obj(train_space_path)
    #
    # # 导入测试集
    # test_set = read_bunch_obj(test_space_path)
    #
    # print('train词向量矩阵shape: ', train_set.tdm.shape)
    # print('test词向量矩阵shape: ', test_set.tdm.shape)
    #
    # svm = SVC(C=1.0, kernel='linear')
    # # svm = SVC(C=10, kernel='rbf', gamma=1)
    # model = svm.fit(train_set.tdm, train_set.label)
    # print(model)
    # predicted = svm.predict(test_set.tdm)
    # with open('results.txt', 'w', encoding='utf-8') as f:
    #     for i in range(len(predicted)):
    #         f.write(test_set.label[i] + " " + predicted[i] + '\n')
    # metrics_result(test_set.label, predicted)

    M = read_result(svm_results)
    calc_acc(M)

    # svm网格搜索最佳参数
    # svm = SVC()
    #
    # para_range = [0.0001, 0.001, 0.01, 0.1, 1.0, 10, 100, 1000, 10000]
    # para_grid = [
    #     {
    #         'C': para_range,
    #         'kernel': ['linear']},
    #     {
    #         'C': para_range,
    #         'gamma': para_range,
    #         'kernel': ['rbf']}
    # ]
    #
    # grid_search = GridSearchCV(svm, para_grid, cv=10, n_jobs=-1, verbose=1)
    # grid_search.fit(train_set.tdm, train_set.label)
    #
    # print(list(grid_search.best_estimator_.get_params().items()))
    #
    # predicted = grid_search.best_estimator_.predict(test_set.tdm)
    #
    # print(grid_search.best_estimator_)
    #
    # metrics_result(test_set.label, predicted)

    end = time.time()
    print('SVM分类耗时：{}秒'.format(int(end - start)))


if __name__ == '__main__':
    main()
