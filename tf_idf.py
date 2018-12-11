#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: tf_idf
@time: 18-11-18 下午7:57
"""

import os
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

cate = []


def read_corpus(train_path):
    dirs = os.listdir(train_path)
    res = []
    for my_dir in dirs:
        cate.append(my_dir)
        dir_path = os.path.join(train_path, my_dir)
        files = os.listdir(dir_path)
        temp = []
        for file in files:
            file_path = os.path.join(dir_path, file)
            temp.append(read_file(file_path))
        res.append(' '.join(temp))
    return res


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().replace('\n', '')


def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        for line in content:
            f.write(line[0] + ' ' + str(line[1]) + '\n')


def main():
    base_path = '/home/alery/process/'
    train_path = base_path + 'train_corpus_seg/'
    test_path = base_path + 'test_corpus_seg/'
    corpus = read_corpus(train_path)

    # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer()

    # 该类会统计每个词语的tf-idf权值
    transformer = TfidfTransformer()

    # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

    # 获取词袋模型中的所有词语
    word = vectorizer.get_feature_names()
    # print(word)

    # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    weight = tfidf.toarray()

    # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    for i in range(len(weight)):
        print(u"-------这里输出第", cate[i], u"类文本的词语tf-idf权重------")
        d = {}
        for j in range(len(word)):
            if weight[i][j] > 0:
                d[word[j]] = weight[i][j]
                # print(word[j], weight[i][j])
        d_list = sorted(d.items(), key=lambda d1: d1[1], reverse=True)
        # print(d_list)
        write_file(base_path + 'train_word_bag/tf_idf/{}.txt'.format(cate[i]), d_list)


if __name__ == '__main__':
    main()
