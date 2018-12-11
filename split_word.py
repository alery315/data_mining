#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: split_word
@time: 18-11-16 下午7:15
"""
from collections import Counter
from time import time

import jieba
from gensim.models import word2vec
import pandas as pd

BASE_PATH = '/home/alery/sina/sports/'


def get_file_data(path):
    df = pd.read_csv(path, sep=',', header=0)
    df = df.get('content')
    return df
    # with open(path, 'r', encoding='utf-8') as f:
    #     for line in f:
    #         print(line)


def get_word_stop():
    l = []
    with open('stopwords.txt', 'r', encoding='utf-8') as f:
        for line in f:
            l.append(line.replace('\n', ''))
        return l


def main():
    start_time = time()

    stop_word = get_word_stop()
    # print(stop_word)

    contents = get_file_data(BASE_PATH + 'sports_1.csv')
    count = 0
    final = []

    # for content in contents:
    #     try:
    #         if count == 4000:
    #             break
    #         count += 1
    #         # print(content)
    #         seg_list = list(jieba.cut(content, cut_all=False))
    #         # for seg in seg_list:
    #         #     if seg.strip() not in stop_word:
    #         #         final.append(seg)
    #         with open('words3.txt', 'a+', encoding='utf-8') as f:
    #             f.write(' '.join(seg_list))
    #             f.write('\n')
    #         print(count)
    #     except BaseException as e:
    #         print(e.__str__())
        # print(seg_list)

    # c = Counter(final)
    # count = 0
    # for k, v in c.items():
    #     if v >= 20:
    #         count += 1
    # print(c)

    sentences = word2vec.Text8Corpus('words.txt')

    # model = word2vec.Word2Vec(sentences, min_count=20, size=100, workers=8, iter=10)
    #
    # model.save('w2v_model')
    #
    # print(model)

    # model = word2vec.Word2Vec.load('w2v_model')
    #
    # print(model.most_similar('中国', topn=20))
    # print(model.most_similar('东风', topn=20))
    # print(model.most_similar('新能源', topn=20))
    # print(model.most_similar('SUV', topn=20))
    #
    # # print('超过20频次的一共有{}个'.format(count))
    # end_time = time()
    # print('本次运行用时:{}秒'.format(end_time - start_time))


if __name__ == '__main__':
    main()

