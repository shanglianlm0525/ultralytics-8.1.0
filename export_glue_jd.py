# !/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2023/11/7 13:45
# @Author : liumin
# @File : export_glue_jd.py

import os
import numpy as np
import shutil
from pathlib import Path
from ultralytics import YOLO

for dir in ['runs/detect/openvino', 'runs/detect/deploy']:
    if os.path.exists(Path(dir)):
        shutil.rmtree(Path(dir))
        os.makedirs(Path(dir))
    else:
        os.makedirs(Path(dir))


for w_name, n_name, e_name in zip(['stringing_glue_cell4', 'stringing_glue_jd4'],
                ['stringing_glue_cell', 'stringing_glue_jd'],
                ['stringing_glue_0', 'stringing_glue_1']):
    weight_path = 'runs/detect/' + w_name + '/weights/best.pt'
    new_weight_path = weight_path.replace('best.pt', n_name+'.pt')
    shutil.copyfile(weight_path, new_weight_path)
    shutil.copyfile(new_weight_path, os.path.join('runs/detect/deploy', n_name+'.pt'))
    # Load a model
    model = YOLO(new_weight_path)  # load an official model

    # Export the model
    in_width = model.overrides['imgsz']
    if w_name.__contains__("cell"):
        model.export(format='openvino', ch=1, imgsz=(416, 512))
    else:
        model.export(format='openvino', ch=1, imgsz=(896, 1600))

    all_path = 'runs/detect/openvino'
    shutil.copyfile(os.path.join('runs/detect',w_name,'weights/'+n_name+'_openvino_model/', n_name+'.xml'), os.path.join(all_path, e_name+'.xml'))
    shutil.copyfile(os.path.join('runs/detect',w_name,'weights/'+n_name+'_openvino_model/', n_name+'.bin'), os.path.join(all_path, e_name+'.bin'))


