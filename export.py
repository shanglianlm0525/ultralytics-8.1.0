# !/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2023/7/27 10:35
# @Author : liumin
# @File : export.py

import os
import numpy as np
import shutil
from pathlib import Path
from ultralytics import YOLO


for dir in ['runs/detect/openvino_5000', 'runs/detect/openvino_8000', 'runs/detect/deploy']:
    if os.path.exists(Path(dir)):
        shutil.rmtree(Path(dir))
        os.makedirs(Path(dir))
    else:
        os.makedirs(Path(dir))


for w_name, n_name, e_name in zip(['stringing_vi_cell', 'stringing_vi_hdpy5','stringing_vi_hdqs5','stringing_vi_dhd5', 'stringing_vi_jb5', 'stringing_vi_yw5', 'stringing_vi_qj5'],
                ['stringing_vi_cell', 'stringing_vi_hdpy', 'stringing_vi_hdqs', 'stringing_vi_dhd', 'stringing_vi_jb', 'stringing_vi_yw', 'stringing_vi_qj'],
                ['stringing_vi_0', 'stringing_vi_1', 'stringing_vi_2', 'stringing_vi_3', 'stringing_vi_4', 'stringing_vi_5', 'stringing_vi_6']):
    weight_path = 'runs/detect/' + w_name + '/weights/best.pt'
    new_weight_path = weight_path.replace('best.pt', n_name+'.pt')
    shutil.copyfile(weight_path, new_weight_path)
    shutil.copyfile(new_weight_path, os.path.join('runs/detect/deploy', n_name+'.pt'))
    # Load a model
    model = YOLO(new_weight_path)  # load an official model

    # Export the model
    for w_size in [5000, 8000]:
        in_width = model.overrides['imgsz']
        in_height = int(round(in_width / w_size * 4096)) # 5000  8000
        in_height = np.ceil(in_height / 32) * 32

        model.export(format='openvino', ch=1, imgsz=(in_height, in_width))

        all_path = 'runs/detect/openvino_'+str(w_size)
        shutil.copyfile(os.path.join('runs/detect',w_name,'weights/'+n_name+'_openvino_model/', n_name+'.xml'), os.path.join(all_path, e_name+'.xml'))
        shutil.copyfile(os.path.join('runs/detect',w_name,'weights/'+n_name+'_openvino_model/', n_name+'.bin'), os.path.join(all_path, e_name+'.bin'))

