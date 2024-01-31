# !/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2023/6/21 15:14
# @Author : liumin
# @File : train_debris_cell.py

import os
from ultralytics import YOLO

# Load a model
pretrain_weight = "runs/detect/stringing_debris_cell/weights/best.pt"
if os.path.exists(pretrain_weight):
    model = YOLO(pretrain_weight)  # load a pretrained model (recommended for training)
else:
    model = YOLO("weights/yolov8n.pt")  # load a pretrained model (recommended for training)


model.train(data="stringing_debris_cell.yaml", name="stringing_debris_cell", ch=1, epochs=500, cache=True, device='0', imgsz=512)  # train the model



