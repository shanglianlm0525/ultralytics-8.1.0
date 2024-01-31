# !/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2023/11/30 13:28
# @Author : liumin
# @File : export_trt.py

from ultralytics import YOLO

# Load a model
model = YOLO('weights/yolov8n-seg.pt')  # load an official model

# Export the model
model.export(format='onnx', dynamic=True, opset=12) # 第2、3个参数禁止修改






# Load a model
model = YOLO('runs/detect/stringing_glue_cell/weights/best.pt')  # load an official model

# Export the model
model.export(format='onnx', ch=1, dynamic=True, opset=12)