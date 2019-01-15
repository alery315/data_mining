#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: naive_bayes
@time: 18-11-26 下午4:16
"""
import _pickle as pickle
import time

import numpy as np
from sklearn.naive_bayes import MultinomialNB
from data_mining.process.manual_naive_bayes import *

label_dict = {'car': 0, 'food': 1, 'game': 2,
              'health': 3, 'history': 4, 'home': 5,
              'military': 6, 'sports': 7, 'tech': 8, 'yule': 9}


def read_bunch_obj(file):
    with open(file, 'rb') as f:
        bunch = pickle.load(f)
    return bunch


# 计算分类精度：
def metrics_result(actual, predicted):
    print('正确率:{0:.3f}'.format(metrics.precision_score(actual, predicted, average='weighted')))
    print('召回率:{0:0.3f}'.format(metrics.recall_score(actual, predicted, average='weighted')))
    print('f1-score:{0:.3f}'.format(metrics.f1_score(actual, predicted, average='weighted')))


def main():
    np.set_printoptions(suppress=True)

    start_time = time.time()

    # 导入训练集
    train_set = read_bunch_obj(train_space_path)

    # 导入测试集
    test_set = read_bunch_obj(test_space_path)

    print('train词向量矩阵shape:  文档数: ', train_set.tdm.shape[0], '词向量维度: ', train_set.tdm.shape[1])
    print('test词向量矩阵shape: ', '文档数: ', test_set.tdm.shape[0], '词向量维度: ', test_set.tdm.shape[1])

    # 输出词与对应的tf_idf值
    # print(len(train_set.vocabulary))
    # print(train_set.vocabulary.items())

    # l = list(train_set.vocabulary.items())
    # weight = train_set.tdm
    # for i in range(weight.shape[0]):
    #     print('---' * 40)
    #     for j in range(len(l)):
    #         if weight[i, j] > 0:
    #             print(l[j][0], weight[i, j])

    # # 训练分类器：输入词袋向量和分类标签，alpha:0.001 alpha越小，迭代次数越多，精度越高
    clf = MultinomialNB(alpha=0.05).fit(train_set.tdm, train_set.label)

    # # 预测分类结果
    predicted = clf.predict(test_set.tdm)

    # error_num = {}

    # 保存到文件
    with open(nb_results, 'w', encoding='utf-8') as f:
        for i in range(len(predicted)):
            f.write(test_set.label[i] + " " + predicted[i] + '\n')

    metrics_result(test_set.label, predicted)

    confusion_matrix = np.zeros([10, 10])

    for label, file_name, expect_cate in zip(test_set.label, test_set.filenames, predicted):
        confusion_matrix[label_dict[label]][label_dict[expect_cate]] += 1

    calc_acc(confusion_matrix)

    end_time = time.time()
    print('贝叶斯分类耗时：{}秒'.format(int(end_time - start_time)))


if __name__ == '__main__':
    main()
