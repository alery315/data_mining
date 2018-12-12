#!/usr/bin/env python
# encoding: utf-8

"""
@author: alery
@file: due_process
@time: 18-11-18 下午8:40
"""
import os
import re

BASE_PATH = '/home/alery/sina/tech/'


def all_dirs(path):
    for root, dirs, files in os.walk(path):
        return dirs


def all_files(path):
    for root, dirs, files in os.walk(path):
        return files


def get_content(files):
    for file in files:
        file = BASE_PATH + file
        print(file)
        contents = []
        # df = pd.read_csv(file, sep=',', header=0)
        # df = df.get('content')
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                line = re.sub(".ct_hqimg.*18px; }", '', str(line))
                line = re.sub("\"SINA_TEXT_PAGE_INFO.*} }\);", '', str(line))
                line = re.sub("SinaPage.loadWidget.*} }\);", '', str(line))
                line = re.sub("widgetadd.*} }\);", '', str(line))
                line = re.sub("\.ct_hqimg.*18px; }", '', str(line))
                line = re.sub("\.tech-quotation.*important;}", '', str(line))
                line = re.sub("\(function\(\).*}\)\(\);", '', str(line))
                line = line.replace('\n', '')
                contents.append(line)
            write_to_csv(file, contents)


def write_to_csv(file, contents):
    with open(file, 'w', encoding='utf-8') as f:
        f.writelines([line + '\n' for line in contents])


def main():
    files = all_files(BASE_PATH)
    get_content(files)


if __name__ == '__main__':
    main()
