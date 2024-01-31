# !/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2023/4/23 11:08
# @Author : liumin
# @File : proc_stringing_el_data.py

import json
import numpy as np
import os
import sys
import re
import shutil
import cv2
from glob2 import glob
from tqdm import tqdm
import random


root_path = '/home/liumin/data/botrong/stringing_el/'
img_suffix = '.jpg'
anno_suffix = '.json'
label_suffix = '.txt'

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



def moveValidData():
    repeat_list = []
    img_path = os.path.join(root_path, 'images/train2017')
    xml_path = os.path.join(root_path, 'annotations/train2017')
    org_path = os.path.join(root_path, 'org')
    imglist = []
    get_file_path(org_path, imglist)
    for imgPath in tqdm(imglist):
        xmlPath = imgPath.replace(img_suffix, anno_suffix)
        imgname = os.path.basename(imgPath)
        xmlname = imgname.replace(img_suffix, anno_suffix)
        if os.path.exists(imgPath) and os.path.exists(xmlPath):
            if os.path.exists(os.path.join(img_path, imgname)) or os.path.exists(os.path.join(xml_path, xmlname)):
                repeat_list.append(imgname)
                continue
            # print(imgPath, xmlPath)
            shutil.copyfile(imgPath, os.path.join(img_path, imgname))
            shutil.copyfile(xmlPath, os.path.join(xml_path, xmlname))

    print('repeat_list', repeat_list)


def convert_json_label_to_yolov_seg_label():
    import glob
    import numpy as np
    json_path = r"C:\Users\jianming_ge\Desktop\code\handle_dataset\water_street";
    json_files = glob.glob(json_path + "/*.json")
    for json_file in json_files:
        # if json_file != r"C:\Users\jianming_ge\Desktop\code\handle_dataset\water_street\223.json":
        #     continue
        print(json_file)
        f = open(json_file)
        json_info = json.load(f)
        # print(json_info.keys())
        img = cv2.imread(os.path.join(json_path, json_info["imagePath"]))
        height, width, _ = img.shape
        np_w_h = np.array([[width, height]], np.int32)
        txt_file = json_file.replace(".json", ".txt")
        f = open(txt_file, "a")
        for point_json in json_info["shapes"]:
            txt_content = ""
            np_points = np.array(point_json["points"], np.int32)
            norm_points = np_points / np_w_h
            norm_points_list = norm_points.tolist()
            txt_content += "0 " + " ".join([" ".join([str(cell[0]), str(cell[1])]) for cell in norm_points_list]) + "\n"
            f.write(txt_content)


lbls = {'xh': 0, 'yl': 1, 'sp': 2, 'pp':3 }

def transJson2Yolo():
    lbl_num = [0] * len(lbls)
    hw_ratios = [[0] for _ in lbls]

    imglist = glob(os.path.join(root_path, 'images/train2017', "*"+img_suffix))
    for imgpath in tqdm(imglist):
        xmlpath = imgpath.replace("images", "annotations").replace(img_suffix, anno_suffix)
        labelpath = imgpath.replace("images", "labels").replace(img_suffix, label_suffix)
        # print(imgpath, xmlpath, labelpath)

        image = cv2.imread(imgpath)
        gheight, gwidth, _ = image.shape
        np_w_h = np.array([[gwidth, gheight]], np.int32)

        with open(xmlpath, "r") as f:
            json_data = f.read()
        json_info = json.loads(json_data)

        seg_txt = open(labelpath, 'a')
        for point_json in json_info["shapes"]:
            if point_json["label"] not in lbls:
                print(point_json["label"], imgpath)
                continue

            cls = str(lbls[point_json["label"]])
            txt_content = ""
            np_points = np.array(point_json["points"], np.int32)
            y1, x1, y2, x2 = np.min(np_points[:, 1]), np.min(np_points[:, 0]), np.max(np_points[:, 1]), np.max(np_points[:, 0])
            norm_points = np_points / np_w_h
            norm_points_list = norm_points.tolist()
            txt_content += cls + " " + " ".join([" ".join([str(cell[0]), str(cell[1])]) for cell in norm_points_list]) + "\n"
            seg_txt.write(txt_content)

            lbl_num[int(cls)] = lbl_num[int(cls)] + 1
            hw_ratios[int(cls)].append(max((x2 - x1) / (y2 - y1), (y2 - y1) / (x2 - x1)))
        seg_txt.close()

    print(lbl_num)
    print('------')
    for hw_ratio in hw_ratios:
        print(min(hw_ratio[1:]), max(hw_ratio[1:]))

if __name__ == '__main__':
    # moveValidData()
    transJson2Yolo()