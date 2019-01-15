#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: manual_naive_bayes
@time: 18-12-6 下午4:05
"""
import _pickle as pickle
import time
from functools import partial
from multiprocessing.pool import Pool
import multiprocessing
import numpy as np
from data_mining.config import *

#  分类映射字典与反转字典
from sklearn import metrics

label_dict = {'car': 0, 'food': 1, 'game': 2,
              'health': 3, 'history': 4, 'home': 5,
              'military': 6, 'sports': 7, 'tech': 8, 'yule': 9}
label_dict_reverse = dict(zip(label_dict.values(), label_dict.keys()))


def readfile(path):
    with open(path, "r", encoding='utf-8') as fp:
        return fp.read().split(' ')


def read_bunch_obj(file):
    with open(file, 'rb') as f:
        bunch = pickle.load(f)
    return bunch


def calc_cate_probability(label):
    #  计算分类比率P(yi)
    cate_probability = {}
    label_set = set(label)
    for l in label_set:
        cate_probability[label_dict[l]] = label.count(l) / len(label)
    # print(cate_probability)
    return cate_probability


def calc_condition_probability(vocabulary, tf_idf, label, cate_probability):
    #  计算条件概率P(xi|yi)
    #  分类数 * 词向量维度
    condition_probability = np.zeros([len(cate_probability), len(vocabulary)])
    #  分类数 * 1,这个用来归一化条件概率矩阵
    sum_weight = np.zeros([len(cate_probability), 1])
    doc_num = tf_idf.shape[0]
    for i in range(doc_num):
        condition_probability[label_dict[label[i]]] += tf_idf[i]
        sum_weight[label_dict[label[i]]] = np.sum(condition_probability[label_dict[label[i]]])

    # print('sum_weight:', sum_weight)
    condition_probability /= sum_weight

    vocabulary_reverse = dict(zip(vocabulary.values(), vocabulary.keys()))

    #  保存到文件中
    with open(condition_probability_path, 'w', encoding='utf-8') as f:
        for i in range(len(condition_probability)):
            for j in range(len(condition_probability[i])):
                f.write(vocabulary_reverse[j] + ' ' + str(condition_probability[i][j]) + '\n')
    return condition_probability


# 读入p(xi|yi)矩阵
def read_condition_probability(row, col):
    condition_probability = np.zeros([row, col])
    with open(condition_probability_path, 'r', encoding='utf-8') as f:
        content = f.readlines()
        num = 0
        for line in content:
            x = int(num / col)
            y = num % col
            condition_probability[x, y] = line.strip().split(' ')[-1]
            num += 1
    return condition_probability


def predict_one(index, condition_probability, cate_probability, test_set, label_list):
    pred_value = 0
    pred_class = 0

    for i in range(len(cate_probability)):
        temp = np.sum(test_set.tdm[index] * condition_probability[i] * cate_probability[i])
        if temp > pred_value:
            pred_value = temp
            pred_class = i

    label_list.append(test_set.label[index] + ' ' + str(label_dict_reverse[pred_class]))

    #  在这里解包的时候,由于dict的不确定性,导致出来的标签是乱的,所以先排序一下,让它和初始化的label_dict相同顺序
    # for (keyVect, keyClass) in zip(condition_probability, sorted(cate_probability)):
    #     temp = np.sum(vector * keyVect * cate_probability[keyClass])
    #     if temp > pred_value:
    #         pred_value = temp
    #         pred_class = keyClass


def predict(test_set, cate_probability, condition_probability):
    confusion_matrix = np.zeros([len(cate_probability), len(cate_probability)])

    label_list = multiprocessing.Manager().list()

    pool = Pool()
    partial_work = partial(predict_one, condition_probability=condition_probability, cate_probability=cate_probability
                           , test_set=test_set, label_list=label_list)
    pool.map(partial_work, [i for i in range(len(test_set.label))])
    pool.close()
    pool.join()

    for line in label_list:
        labels = line.split(' ')
        one = labels[0].strip()
        two = labels[1].strip()
        confusion_matrix[label_dict[one], label_dict[two]] += 1

    return confusion_matrix


#  计算分类精度
def calc_acc(confusion_matrix):
    print('-' * 30, '分类混淆矩阵为:', '-' * 30)
    print(confusion_matrix)
    print('-' * 75)
    n = len(confusion_matrix)
    acc_all = 0
    recall_all = 0
    for i in range(n):
        rows, cols = sum(confusion_matrix[i]), sum(confusion_matrix[r][i] for r in range(n))
        try:
            acc = (confusion_matrix[i][i] / float(cols))
            acc_all += acc
            recall = (confusion_matrix[i][i] / float(rows))
            recall_all += recall
            print('class: ', label_dict_reverse[i], 'acc: %.3f' % acc, 'recall: %.3f' % recall)
        except ZeroDivisionError:
            print('acc: %s' % 0, 'recall: %s' % 0)
    acc_all /= len(confusion_matrix)
    recall_all /= len(confusion_matrix)
    print('正确率: %.3f' % acc_all)
    print('召回率: %.3f' % recall_all)
    print('f1-force: ', round(2 * acc_all * recall_all / (acc_all + recall_all), 3))


# 计算分类精度：
def metrics_result(actual, predicted):
    print('正确率:{0:.3f}'.format(metrics.precision_score(actual, predicted, average='weighted')))
    print('召回率:{0:0.3f}'.format(metrics.recall_score(actual, predicted, average='weighted')))
    print('f1-score:{0:.3f}'.format(metrics.f1_score(actual, predicted, average='weighted')))


def main():
    # 设置混淆矩阵不用科学计数法输出
    np.set_printoptions(suppress=True)
    start = time.time()

    # 导入训练集
    train_set = read_bunch_obj(train_space_path)

    # 导入测试集
    test_set = read_bunch_obj(test_space_path)

    print('train词向量矩阵shape:  文档数: ', train_set.tdm.shape[0], '词向量维度: ', train_set.tdm.shape[1])
    print('test词向量矩阵shape: ', '文档数: ', test_set.tdm.shape[0], '词向量维度: ', test_set.tdm.shape[1])

    label = train_set.label
    tf_idf = train_set.tdm
    vocabulary = train_set.vocabulary

    #  训练贝叶斯
    cate_probability = calc_cate_probability(label)
    # # 读入条件概率
    condition_probability = read_condition_probability(len(cate_probability), len(vocabulary))
    # condition_probability = calc_condition_probability(vocabulary, tf_idf, label, cate_probability)

    end = time.time()
    print('读入矩阵cost {0:.2f} s'.format(end - start))

    #  测试集分类
    start = time.time()

    # 返回预测标签集合与混淆矩阵
    confusion_matrix = predict(test_set, cate_probability, condition_probability)
    calc_acc(confusion_matrix)

    end = time.time()
    print('测试分类cost {0:.2f} s'.format(end - start))


if __name__ == '__main__':
    main()
