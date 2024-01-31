# !/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2023/6/21 15:14
# @Author : liumin
# @File : train_model.py

from ultralytics import YOLO

# Load a model
# model = YOLO("yolov8n.yaml")  # build a new model from scratch
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
# Use the model

# model.train(data="stringing_vi_cell.yaml", name="stringing_vi_cell", ch=1, epochs=500, cache=True, device='0', imgsz=512)  # train the model
model.train(data="stringing_vi_cell.yaml", name="stringing_vi_cell", ch=1, epochs=500, cache=True, device='0', imgsz=1024)  # train the model



'''
metrics = model.val()  # evaluate model performance on the validation set
results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image
path = model.export(format="onnx")  # export the model to ONNX format
'''