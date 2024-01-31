# !/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2023/4/18 16:00
# @Author : liumin
# @File : proc_stringing_vi_yw_data.py

import os
import sys
import re
import shutil
import cv2
from glob2 import glob
from tqdm import tqdm
import random

org_path = '/home/liumin/botrong/stringing_vi/'
root_path = '/home/liumin/botrong/stringing_vi_hdpy/'
img_suffix = '.bmp'
anno_suffix = '.xml'
label_suffix = '.txt'

lbls = {'hdpy': 0}


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



def moveValidData(add_empty=False, ratio=0.01):
    repeat_list = []
    img_path = os.path.join(root_path, 'images/train2017')
    xml_path = os.path.join(root_path, 'annotations/train2017')
    all_path = os.path.join(org_path, 'org')
    imglist = []
    emptylist = []
    valid_num = 0
    get_file_path(all_path, imglist)
    for imgPath in tqdm(imglist):
        xmlPath = imgPath.replace(img_suffix, anno_suffix)
        imgname = os.path.basename(imgPath)
        xmlname = imgname.replace(img_suffix, anno_suffix)
        if os.path.exists(imgPath) and os.path.exists(xmlPath):
            if os.path.exists(os.path.join(img_path, imgname)) or os.path.exists(os.path.join(xml_path, xmlname)):
                repeat_list.append(imgname)
                continue
            # print(imgPath, xmlPath)
            # print(os.path.join(img_path, imgname))
            # print(os.path.join(xml_path, xmlname))
            flag = False
            bbox = get_annotations(xmlPath)
            for bb in bbox:
                if bb[0] in lbls:
                    flag = True
                else:
                    if add_empty:
                        emptylist.append(imgPath)
            if flag:
                shutil.copyfile(imgPath, os.path.join(img_path, imgname))
                shutil.copyfile(xmlPath, os.path.join(xml_path, xmlname))
                valid_num = valid_num + 1

    if add_empty:
        random.shuffle(emptylist)
        for imgPath in tqdm(emptylist[:int(valid_num * ratio)]):
            xmlPath = imgPath.replace(img_suffix, anno_suffix)
            imgname = os.path.basename(imgPath)
            xmlname = imgname.replace(img_suffix, anno_suffix)
            shutil.copyfile(imgPath, os.path.join(img_path, imgname))
            shutil.copyfile(xmlPath, os.path.join(xml_path, xmlname))

    print('repeat_list', repeat_list)


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




def transVoc2Yolo():
    lbl_num = [0] * len(lbls)
    hw_ratios = [[0] for _ in lbls]

    imglist = glob(os.path.join(root_path, 'images/train2017', "*"+img_suffix))
    for imgpath in tqdm(imglist):
        xmlpath = imgpath.replace("images", "annotations").replace(img_suffix, anno_suffix)
        labelpath = imgpath.replace("images", "labels").replace(img_suffix, label_suffix)
        # print(imgpath, xmlpath, labelpath)

        image = cv2.imread(imgpath)
        if image is None:
            print(imgpath)
        gheight, gwidth, _ = image.shape
        bbox = get_annotations(xmlpath)

        seg_txt = open(labelpath, 'a')
        for bb in bbox:
            if bb[0] not in lbls:
                # print(bb[0], imgpath)
                continue
            
            cls = str(lbls[bb[0]])
            bb[1], bb[2], bb[3], bb[4] = max(bb[1], 0), max(bb[2], 0), min(bb[3], gwidth - 1), min(bb[4], gheight - 1)
            lbl_num[int(cls)] = lbl_num[int(cls)] + 1
            x_center = str((bb[1] + bb[3]) * 0.5 / gwidth)
            y_center = str((bb[2] + bb[4]) * 0.5 / gheight)
            width = str((bb[3] - bb[1]) * 1.0 / gwidth)
            height = str((bb[4] - bb[2]) * 1.0 / gheight)
            seg_txt.write(cls + ' ' + x_center + ' ' + y_center + ' ' + width + ' ' + height + '\n')
            if (bb[3] - bb[1]) < 0 or bb[4] - bb[2] < 0:
                print(10*'*', bb[1], bb[2], bb[3], bb[4])
                print(imgpath)
                assert 1 == 2
            hw_ratios[int(cls)].append(max((bb[3] - bb[1]) / (bb[4] - bb[2]), (bb[4] - bb[2]) / (bb[3] - bb[1])))
        seg_txt.close()


    print(lbl_num)
    print('------')
    for hw_ratio in hw_ratios:
        print(min(hw_ratio[1:]), max(hw_ratio[1:]))


def splitTrainVal(p=0.2):
    img_path = os.path.join(root_path, 'images/train2017')
    xml_path = os.path.join(root_path, 'labels/train2017')

    val_img_path = os.path.join(root_path, 'images/val2017')
    val_xml_path = os.path.join(root_path, 'labels/val2017')
    imglist = os.listdir(img_path)
    print('total:', len(imglist))
    for imgname in imglist:
        imgpath = os.path.join(img_path, imgname)
        if random.random() < p:
            xmlname = imgname.replace(img_suffix, label_suffix)
            # shutil.copyfile(imgpath, os.path.join(val_img_path, imgname))
            # shutil.copyfile(os.path.join(xml_path, xmlname), os.path.join(val_xml_path, xmlname))
            print(imgpath, os.path.join(val_img_path, imgname))
            print(os.path.join(xml_path, xmlname), os.path.join(val_xml_path, xmlname))
            shutil.move(imgpath, os.path.join(val_img_path, imgname))
            shutil.move(os.path.join(xml_path, xmlname), os.path.join(val_xml_path, xmlname))


if __name__ == '__main__':
    moveValidData(add_empty=False)
    transVoc2Yolo()
