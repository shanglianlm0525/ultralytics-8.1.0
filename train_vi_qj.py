# !/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2023/6/21 15:14
# @Author : liumin
# @File : train_model.py
import os
from ultralytics import YOLO

# Load a model
pretrain_weight = "runs/detect/stringing_vi_qj_pretrain/weights/best.pt"
if os.path.exists(pretrain_weight):
    model = YOLO(pretrain_weight)  # load a pretrained model (recommended for training)
else:
    model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)


model.train(data="stringing_vi_qj.yaml", name="stringing_vi_qj", ch=1, epochs=500, cache=True, device='0', imgsz=1600)  # train the model


'''
metrics = model.val()  # evaluate model performance on the validation set
results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image
path = model.export(format="onnx")  # export the model to ONNX format
'''