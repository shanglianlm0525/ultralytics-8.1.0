# !/usr/bin/env python
# -- coding: utf-8 --

# @Time : 2023/6/21 15:14
# @Author : liumin
# @File : train_debris_sp.py

import os
from ultralytics import YOLO

# Load a model
pretrain_weight = "runs/detect/stringing_debris_sp/weights/best.pt"
if os.path.exists(pretrain_weight):
    model = YOLO(pretrain_weight)  # load a pretrained model (recommended for training)
else:
    model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

model.train(data="stringing_debris_sp.yaml", name="stringing_debris_sp", ch=1, epochs=500, cache=True, device='1', imgsz=640)  # train the model # 1600



