#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: config
@time: 18-12-11 下午9:28
"""
# 每个文件取的最大值,我分的是每个文件5000条
MAX_LINE = 50000
# 线程数
THREAD_NUM = 32
# 切分为一个一个小文件,每一类中最大的数
MAX_FILES = 1000000
# 筛选训练与测试的文件数,当前还是每个文件5000条,四个就是每类2W
REMAINING = 4
# 留下一部分文件来测试
RES_FILES = 1000

# 文件存放目录base
base_path = '/home/alery/process/'

# 还未分词的语料库
train_corpus_path = base_path + 'train_corpus/'
test_corpus_path = base_path + 'test_corpus/'

# 分词后存放

# train_corpus_seg_path = base_path + 'train_corpus_seg/'
# test_corpus_seg_path = base_path + 'test_corpus_seg/'
# 这里存放的是卡方提取后的
train_corpus_seg_path = base_path + 'train_corpus_seg/'
test_corpus_seg_path = base_path + 'test_corpus_seg/'

# 停用词存放 这个我在项目里了,相对路径
stop_word_path = base_path + 'stop_words.txt'

# 保存tf_idf
save_tfidf_path = base_path + 'train_word_bag/tf_idf/'

# 存放到bunch
train_bunch_path = base_path + 'train_word_bag/train_set.dat'
test_bunch_path = base_path + 'test_word_bag/test_set.dat'

# 保存卡方以及卡方提取后的语料库
chi_path = base_path + 'chi_square/'
train_corpus_chi_path = base_path + 'train_corpus_seg_chi/'
test_corpus_chi_path = base_path + 'test_corpus_seg_chi/'

# 保存tf_idf相关数据到bunch
train_space_path = base_path + 'train_word_bag/train_space.dat'
test_space_path = base_path + 'test_word_bag/test_space.dat'

# svm 条件概率矩阵
condition_probability_path = base_path + 'train_word_bag/condition_probability.txt'
