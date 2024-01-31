# !/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2023/4/18 16:00
# @Author : liumin
# @File : proc_stringing_vi_checkdata.py

import os
import sys
import re
import shutil
import cv2
from glob2 import glob
from tqdm import tqdm
import random
import collections

root_path = '/home/liumin/botrong/stringing_vi/'
img_suffix = '.bmp'
anno_suffix = '.xml'
label_suffix = '.txt'

# lbls = {'hdpy': 0, 'yw': 1, 'hdqs': 2, 'jb':3, 'qj':4, 'hdhf':5, 'hdlj':6 }
lbls = {'hdpy': 0, 'yw': 1, 'hdqs': 2, 'jb':3, 'qj':4, 'dhd':4 }


def get_file_path(root_path, file_list):
    #获取该目录下所有的文件名称和目录名称
    dir_or_files = os.listdir(root_path)
    for dir_file in dir_or_files:
        #获取目录或者文件的路径
        dir_file_path = os.path.join(root_path,dir_file)
        #判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            #递归获取所有文件和目录的路径
             get_file_path(dir_file_path, file_list)
        else:
            if dir_file_path.endswith(img_suffix):
                file_list.append(dir_file_path)


pattens = ['name', 'xmin', 'ymin', 'xmax', 'ymax']

def get_annotations(xml_path):
    bbox = []
    with open(xml_path, 'r') as f:
        text = f.read().replace('\n', 'return')
        p1 = re.compile(r'(?<=<object>)(.*?)(?=</object>)')
        result = p1.findall(text)
        for obj in result:
            tmp = []
            for patten in pattens:
                p = re.compile(r'(?<=<{}>)(.*?)(?=</{}>)'.format(patten, patten))
                if patten == 'name':
                    tmp.append(p.findall(obj)[0])
                else:

                    tmp.append(int(float(p.findall(obj)[0])))
            bbox.append(tmp)
    return bbox


def checkdata():
    repeat_list = []
    error_list = []
    org_path = os.path.join(root_path, 'org')
    imglist = []
    get_file_path(org_path, imglist)
    for imgPath in tqdm(imglist):
        xmlPath = imgPath.replace(img_suffix, anno_suffix)

        image = cv2.imread(imgPath)
        if image is None:
            error_list.append(imgPath)
            continue
        gheight, gwidth, _ = image.shape
        try:
            bbox = get_annotations(xmlPath)
        except Exception as e:
            print(e)
            error_list.append(xmlPath)


    print('repeat_list', repeat_list)
    print('error_list', error_list)


if __name__ == '__main__':
    checkdata()
