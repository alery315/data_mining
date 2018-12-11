#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: naive_bayes
@time: 18-11-26 下午4:16
"""
import _pickle as pickle
from sklearn.naive_bayes import MultinomialNB
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

    print(len(train_set.vocabulary))
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

    error_num = {}

    for label, file_name, expect_cate in zip(test_set.label, test_set.filenames, predicted):
        if label != expect_cate:
            if label not in error_num:
                error_num[label] = {}
                error_num[label][expect_cate] = 1
            else:
                if expect_cate not in error_num[label]:
                    error_num[label][expect_cate] = 1
                else:
                    error_num[label][expect_cate] += 1

            # print(file_name, ": 实际类别:", label, " -->预测类别:", expect_cate)

    print('-' * 60, "错误的数量为", '-' * 60)
    for k, v in error_num.items():
        print(k, v, sum([num for num in v.values()]))
    metrics_result(test_set.label, predicted)


if __name__ == '__main__':
    main()
