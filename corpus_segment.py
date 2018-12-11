#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: corpus_segment
@time: 18-11-24 下午8:13
"""
import math
import os
import time
from functools import partial
from multiprocessing.pool import Pool
import random

import jieba
import threadpool

MAX_LINE = 50000
THREAD_NUM = 32
MAX_FILES = 1000000
REMAINING = 4
RES_FILES = 100


# 保存至文件
def savefile(savepath, content):
    # print(content)
    with open(savepath, "a+", encoding='utf-8') as fp:
        fp.write(content)


# 读取文件
def readfile(path):
    content = []
    with open(path, "r", encoding='utf-8') as fp:
        count = 0
        for line in fp:
            if count == MAX_LINE:
                break
            count += 1
            content.append(line)
        # content = fp.read()
    return content


# 读取停用词
def read_stop_word():
    with open('stopwords.txt', 'r', encoding='utf-8') as f:
        words = f.read().split('\n')
        d = {}
        for word in words:
            d[word] = 1
        return d


def corpus_segment(corpus_path, seg_path):
    cate_list = os.listdir(corpus_path)  # 获取corpus_path下的所有子目录

    # 使用多线程
    # pool = threadpool.ThreadPool(THREAD_NUM)
    # paras = [([cate, corpus_path, seg_path], None) for cate in cate_list]
    # # print(paras)
    # requests = threadpool.makeRequests(split_word_by_cate, paras)
    # [pool.putRequest(req) for req in requests]
    # pool.wait()

    # 使用多进程
    pool = Pool()
    partial_work = partial(split_word_by_cate, corpus_path=corpus_path, seg_path=seg_path)
    pool.map(partial_work, cate_list)
    pool.close()
    pool.join()


def split_word_by_cate(mydir, corpus_path, seg_path):
    class_path = corpus_path + mydir + "/"  # 拼出分类子目录的路径如：train_corpus/art/
    seg_dir = seg_path + mydir + "/"  # 拼出分词后存贮的对应目录路径如：train_corpus_seg/art/

    if not os.path.exists(seg_dir):  # 是否存在分词目录，如果没有则创建该目录
        os.makedirs(seg_dir)

    file_list = os.listdir(class_path)  # 获取未分词语料库中某一类别中的所有文本

    # 分词去除停用词
    for file_path in file_list:
        fullname = class_path + file_path  # 拼出文件名全路径如：train_corpus/art/21.txt
        content = readfile(fullname)  # 读取文件内容
        for line in content:
            line = str(line)

            # 初步处理
            line = line.replace("\r\n", "")  # 删除换行
            line = line.replace(" ", "")  # 删除空行、多余的空格
            line = line.replace("，", "")
            line = line.replace("。", "")
            line = line.replace("、", "")
            content_seg = jieba.cut(line, cut_all=False)  # 为文件内容分词

            # 这里去除停用词
            stop_words = read_stop_word()
            seg = list(content_seg)
            final_content = []
            # final_content = seg
            for word in seg:
                if word not in stop_words and '%' not in word and '.' not in word and not word.isnumeric():
                    final_content.append(word)
            # print(final_content)
            savefile(seg_dir + file_path, " ".join(final_content))  # 将处理后的文件保存到分词后语料目录

    print("{}中文语料分词结束！".format(mydir))


def split_word_by_file(class_path, seg_dir, file_path):
    fullname = class_path + file_path  # 拼出文件名全路径如：train_corpus/art/21.txt
    content = readfile(fullname)  # 读取文件内容
    for line in content:
        line = str(line)

        # 初步处理
        line = line.replace("\r\n", "")  # 删除换行
        line = line.replace(" ", "")  # 删除空行、多余的空格
        line = line.replace("，", "")
        line = line.replace("。", "")
        line = line.replace("、", "")
        content_seg = jieba.cut(line, cut_all=False)  # 为文件内容分词

        # 这里去除停用词
        stop_words = read_stop_word()
        seg = list(content_seg)
        final_content = []
        for word in seg:
            if word not in stop_words:
                final_content.append(word)
        # print(final_content)
        savefile(seg_dir + file_path, " ".join(final_content))  # 将处理后的文件保存到分词后语料目录


def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def split_more_files(path):
    dirs = os.listdir(path)
    for mydir in dirs:
        dir_path = path + mydir + "/"
        files = os.listdir(dir_path)
        count = 0
        for file in files:
            t = file.split('.')[0]

            # 如果是数字命名的就跳过
            if t.isdigit():
                continue

            file = dir_path + file
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    if count == MAX_FILES:
                        break
                    write_file(dir_path + str(count) + '.txt', line)
                    count += 1
            os.remove(file)
        print(mydir, '类文件切分结束!')


def reserve_files(path):
    dirs = os.listdir(path)
    for mydir in dirs:
        dir_path = path + mydir + "/"
        files = os.listdir(dir_path)
        res_file = -1
        for file in files:
            res_file += 1
            if res_file < RES_FILES:
                continue
            file = dir_path + file
            os.remove(file)
        print(mydir, '类文件保留结束!')


def split_train_test(train_path, test_path, remaining=-1):
    if remaining == -1:
        cate_num_dict = {}
        dirs = os.listdir(train_path)
        for my_dir in dirs:
            dir_path = os.path.join(train_path, my_dir)
            files = os.listdir(dir_path)
            files.sort(key=lambda name: int(name.split('_')[-1].split('.')[0]))
            # print(files)
            length = len(files)
            num = int(length / 2)
            if my_dir not in cate_num_dict:
                cate_num_dict[my_dir] = num
            for file in [files[i] for i in range(num, length)]:
                print('删除了', os.path.join(dir_path, file))
                os.remove(os.path.join(dir_path, file))
        dirs = os.listdir(test_path)
        for my_dir in dirs:
            dir_path = os.path.join(test_path, my_dir)
            files = os.listdir(dir_path)
            files.sort(key=lambda name: int(name.split('_')[-1].split('.')[0]))
            length = len(files)
            num = int(length / 2)
            if my_dir not in cate_num_dict:
                cate_num_dict[my_dir] = num
            for file in [files[i] for i in range(num)]:
                print('删除了', os.path.join(dir_path, file))
                os.remove(os.path.join(dir_path, file))
    else:
        dirs = os.listdir(train_path)
        for my_dir in dirs:
            dir_path_tr = os.path.join(train_path, my_dir)
            dir_path_te = os.path.join(test_path, my_dir)
            # 训练集删除
            files = os.listdir(dir_path_tr)
            files.sort(key=lambda name: int(name.split('_')[-1].split('.')[0]))
            pos = random.sample(range(0, len(files) - 1), remaining * 2)
            for i in range(len(files)):
                if i in pos[:remaining]:
                    continue
                print('删除了', os.path.join(dir_path_tr, files[i]))
                os.remove(os.path.join(dir_path_tr, files[i]))
            # 测试集删除
            files = os.listdir(dir_path_te)
            files.sort(key=lambda name: int(name.split('_')[-1].split('.')[0]))
            print(pos[:remaining], pos[remaining:])
            for i in range(len(files)):
                if i in pos[remaining:]:
                    continue
                print('删除了', os.path.join(dir_path_te, files[i]))
                os.remove(os.path.join(dir_path_te, files[i]))


def main():
    start_time = time.time()
    base_path = '/home/alery/process/'
    train_path = base_path + 'train_corpus_seg/'
    test_path = base_path + 'test_corpus_seg/'

    # # 对训练集进行分词
    # corpus_path = base_path + "train_corpus/"  # 未分词分类语料库路径
    # seg_path = base_path + "train_corpus_seg/"  # 分词后分类语料库路径
    # corpus_segment(corpus_path, seg_path)

    # # 对测试集进行分词
    # corpus_path = base_path + "test_corpus/"  # 未分词分类语料库路径
    # seg_path = base_path + "test_corpus_seg/"  # 分词后分类语料库路径
    # corpus_segment(corpus_path, seg_path)

    # # 选择训练集与测试集
    # split_train_test(train_path, test_path, REMAINING)
    # # 不加参数表示对半分
    # split_train_test(train_path, test_path)

    # # 切分为多个文件
    # split_more_files(train_path)
    # split_more_files(test_path)

    # 保留部分文件
    reserve_files(train_path)
    reserve_files(test_path)

    end_time = time.time()
    print('分词耗时：{}秒'.format(int(end_time - start_time)))


if __name__ == '__main__':
    main()
