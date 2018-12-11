#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: chi_square
@time: 18-11-30 下午4:20
"""
import os
import time

from data_mining.config import *

sum_dict = {}
RESERVED_NUM = 10000


def write_file(path, content):
    with open(path, 'a+', encoding='utf-8') as f:
        f.write(content + '\n')


def read_file(path, sep):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().split(sep)


def read_chi_square(path):
    with open(path, 'r', encoding='utf-8') as f:
        count = 1
        d = {}
        for line in f:
            if count == RESERVED_NUM:
                return d
            count += 1
            d[line] = 1
        return d


def calc_word_times(path, chi_path):
    dirs = os.listdir(path)
    for my_dir in dirs:
        dir_path = os.path.join(path, my_dir)
        files = os.listdir(dir_path)
        chi_file_path = os.path.join(chi_path, my_dir) + '.txt'
        d = {}
        for file in files:
            file_path = os.path.join(dir_path, file)
            s = set(read_file(file_path, sep=' '))
            for word in s:
                if word not in d:
                    d[word] = 1
                else:
                    d[word] += 1
        # 这里可以控制删除一些词,做一些处理!!!!!
        sorted_list = sorted(d.items(), key=lambda d1: d1[1], reverse=True)
        for item in sorted_list:
            if item[1] == 2:
                break
            if len(item[0]) > 1 and '%' not in item[0] and '.' not in item[0] and not item[0].isnumeric():
                write_file(chi_file_path, item[0] + ' ' + str(item[1]))
        print('{}类词频写入完成!'.format(my_dir))


def read_word_times(path):
    files = os.listdir(path)
    for file in files:
        cate = os.path.splitext(file)[0]
        if 'chi' in cate:
            continue
        if cate not in sum_dict:
            sum_dict[cate] = {}
        file_path = os.path.join(path, file)
        # print(file_path)
        word_times = read_file(file_path, sep='\n')
        # print(word_times)
        for item in word_times:
            if item:
                # print(item)
                word = item.split(' ')[0]
                times = item.split(' ')[1]
                sum_dict[cate][word] = times
                # print(word, ':', times)


def calc_chi_square():
    for cate, d in sum_dict.items():
        # print(cate)
        chi_dict = {}
        cate_num = len(d)
        for word, times in d.items():
            word_out_cate = 0  # B
            no_word_out_cate = 0  # D
            word_in_cate = int(times)  # A
            no_word_in_cate = cate_num - word_in_cate  # C
            for cate_compare in sum_dict:
                if cate_compare != cate:
                    cate_compare_dict = sum_dict[cate_compare]
                    cate_compare_num = len(cate_compare_dict)
                    if word in cate_compare_dict:
                        word_out_cate += int(cate_compare_dict[word])
                        no_word_out_cate += cate_compare_num - int(cate_compare_dict[word])
                    else:
                        no_word_out_cate += cate_compare_num
            chi_dict[word] = ((word_in_cate * no_word_out_cate - word_out_cate * no_word_in_cate) ** 2) / (
                    (word_in_cate + word_out_cate) * (no_word_in_cate + no_word_out_cate))
        sorted_list = sorted(chi_dict.items(), key=lambda d1: d1[1], reverse=True)
        for item in sorted_list:
            write_file('/home/alery/process/chi_square/{}_chi.txt'.format(cate), item[0])
        print(cate, '卡方值写入完成!')


def process_corpus_file(path):
    dirs = os.listdir(path)
    for my_dir in dirs:
        dir_path = os.path.join(path, my_dir)
        d = read_chi_square('/home/alery/process/chi_square/{}_chi.txt'.format(my_dir))
        # print(d)
        files = os.listdir(dir_path)
        for file in files:
            file_path = os.path.join(dir_path, file)
            seg_list = read_file(file_path, sep=' ')
            for seg in seg_list:
                if seg not in d:
                    seg_list.remove(seg)
            with open(file_path, 'w', encoding='utf-8') as f:
                for seg in seg_list:
                    f.write(seg + ' ')
        print(my_dir, '分词处理完成!')


def main():
    start_time = time.time()

    os.system('rm -rf /home/alery/process/test_corpus_seg_chi')
    os.system('rm -rf /home/alery/process/train_corpus_seg_chi')
    os.system('cp -r /home/alery/process/test_corpus_seg /home/alery/process/test_corpus_seg_chi')
    os.system('cp -r /home/alery/process/train_corpus_seg /home/alery/process/train_corpus_seg_chi')

    os.system('rm -rf /home/alery/process/chi_square/*')

    print('文件处理完成!')

    if not os.path.exists(chi_path):
        os.mkdir(chi_path)

    # 计算词频并写入文件
    calc_word_times(test_corpus_path, chi_path)

    # 读入词频
    read_word_times(chi_path)

    # 计算卡方值并写入文件
    calc_chi_square()

    # 处理原有分词文件
    process_corpus_file(train_corpus_chi_path)
    process_corpus_file(test_corpus_chi_path)

    end_time = time.time()
    print('卡方计算与特征提取耗时：{}秒'.format(int(end_time - start_time)))


if __name__ == '__main__':
    main()
