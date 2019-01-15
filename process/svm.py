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
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC,LinearSVC
import multiprocessing
from sklearn.svm import SVC
from sklearn.utils import Bunch

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

    """
    space_bunch:
    tdm matrix,词向量矩阵
    label list,每篇文档对应的标签
    """
    # 导入训练集
    train_set = read_bunch_obj(train_space_path)

    # 导入测试集
    test_set = read_bunch_obj(test_space_path)

    print('train词向量矩阵shape: ', train_set.tdm.shape)
    print('test词向量矩阵shape: ', test_set.tdm.shape)

    # # 多进程的线性svm
    # # onevsrestclassifier 处理多分类,将其他类看做反例
    # # linearSVC线性svm,采用cpu核数的进程数
    # linear_svm = OneVsRestClassifier(LinearSVC(class_weight='balanced'), n_jobs=multiprocessing.cpu_count())
    # model = linear_svm.fit(train_set.tdm, train_set.label)
    #
    # svm_model = Bunch(model=None)
    # svm_model.model = model
    # with open(svm_model_path, 'wb') as f:
    #     pickle.dump(svm_model, f)

    # 读入模型
    svm_model = read_bunch_obj(svm_model_path).model
    print(svm_model)

    predicted = svm_model.predict(test_set.tdm)

    confusion_matrix = np.zeros([CLASS_NUMBER, CLASS_NUMBER])
    for i in range(len(predicted)):
        confusion_matrix[label_dict[test_set.label[i]], label_dict[predicted[i]]] += 1
    calc_acc(confusion_matrix)

    # 单进程的svm
    # svm = SVC(C=1.0, kernel='linear')
    # # svm = SVC(C=10, kernel='rbf', gamma=1)
    # model = svm.fit(train_set.tdm, train_set.label)
    # print(model)

    # predicted = svm.predict(test_set.tdm)
    # with open(svm_results, 'w', encoding='utf-8') as f:
    #     for i in range(len(predicted)):
    #         f.write(test_set.label[i] + " " + predicted[i] + '\n')
    #
    # # 读入结果
    # M = read_result(svm_results)
    # calc_acc(M)

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
