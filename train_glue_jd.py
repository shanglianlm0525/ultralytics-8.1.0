# !/usr/bin/env python
# -- coding: utf-8 --

# @Time : 2023/6/21 15:14
# @Author : liumin
# @File : train_model.py

import os
from ultralytics import YOLO

# Load a model
pretrain_weight = "runs/detect/stringing_glue_jd/weights/best.pt"
if os.path.exists(pretrain_weight):
    model = YOLO(pretrain_weight)  # load a pretrained model (recommended for training)
else:
    model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

model.train(data="stringing_glue_jd.yaml", name="stringing_glue_jd", ch=1, batch=4, epochs=500, cache=True, max_det=1000, device='1', imgsz=1600)  # train the model # 1600



