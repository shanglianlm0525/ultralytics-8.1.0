# !/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2023/8/25 13:33
# @Author : liumin
# @File : all_in_one.py

import os
import random
import shutil
import threading
from tqdm import tqdm
from threading import Thread, Lock
import time
import subprocess
import logging




def action_is_complete(mythreads):
    for mythread in mythreads:
        if mythread.is_alive():
            return False
    return True

def move_data_from_share_local():
    print('begin move_data_from_share_local!')
    os.system('cp -r /home/share_data/ng_check_1/vi_in_cell/vi_in_cell/* /home/liumin/botrong/stringing_vi/org/')
    print('finish move_data_from_share_local!')


def trans_xml_to_txt_1():
    os.system('python proc/proc_stringing_vi_dhd_data.py')

def trans_xml_to_txt_2():
    os.system('python proc/proc_stringing_vi_hdpy_data.py')

def trans_xml_to_txt_3():
    os.system('python proc/proc_stringing_vi_hdqs_data.py')

def trans_xml_to_txt_4():
    os.system('python proc/proc_stringing_vi_jb_data.py')

def trans_xml_to_txt_5():
    os.system('python proc/proc_stringing_vi_yw_data.py')

def trans_xml_to_txt_6():
    os.system('python proc/proc_stringing_vi_qj_data.py')

def trans_xml_to_txt():
    print('begin trans_xml_to_txt!')
    mythreads = []
    mythreads.append(threading.Thread(target=trans_xml_to_txt_1))
    mythreads.append(threading.Thread(target=trans_xml_to_txt_2))
    mythreads.append(threading.Thread(target=trans_xml_to_txt_3))
    mythreads.append(threading.Thread(target=trans_xml_to_txt_4))
    mythreads.append(threading.Thread(target=trans_xml_to_txt_5))
    mythreads.append(threading.Thread(target=trans_xml_to_txt_6))
    for t in mythreads:
        t.start()
    for t in mythreads:
        t.join()

    print('finish trans_xml_to_txt!')


class mythread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.num = 1


def do_train_0():
    print("---begin train hdpy---")
    # os.system('nohup python train_vi_hdpy.py >> stringing_vi_hdpy.log 2>&1 &')

    process = subprocess.Popen(['python', 'train_vi_hdpy.py'])
    process.wait()


class do_train_1(mythread):
    def run(self):
        if lock[self.num].acquire():
            print("---begin train qj---")
            # os.system('nohup python train_vi_qj.py >> stringing_vi_qj.log 2>&1 &')

            process = subprocess.Popen(['python', 'train_vi_qj.py'])
            process.wait()
            lock[(self.num + 1) % N].release()

class do_train_2(mythread):
    def run(self):
        if lock[self.num].acquire():
            print("---begin train jb---")
            # os.system('nohup python train_vi_jb.py >> stringing_vi_jb.log 2>&1 &')

            process = subprocess.Popen(['python', 'train_vi_jb.py'])
            process.wait()
            lock[(self.num + 1) % N].release()


class do_train_3(mythread):
    def run(self):
        if lock[self.num].acquire():
            print("---begin train yw---")
            # os.system('nohup python train_vi_yw.py >> stringing_vi_yw.log 2>&1 &')

            process = subprocess.Popen(['python', 'train_vi_yw.py'])
            process.wait()
            lock[(self.num + 1) % N].release()


class do_train_4(mythread):
    def run(self):
        if lock[self.num].acquire():
            print("---begin train hdqs---")
            # os.system('nohup python train_vi_hdqs.py >> stringing_vi_hdqs.log 2>&1 &')

            process = subprocess.Popen(['python', 'train_vi_hdqs.py'])
            process.wait()
            lock[(self.num + 1) % N].release()


class do_train_5(mythread):
    def run(self):
        if lock[self.num].acquire():
            print("---begin train dhd---")
            # os.system('nohup python train_vi_dhd.py >> stringing_vi_dhd.log 2>&1 &')
            process = subprocess.Popen(['python', 'train_vi_dhd.py'])
            process.wait()
            lock[(self.num + 1) % N].release()


def do_train():
    print('begin do_train!')

    for i in range(N):
        lock.append(Lock())
        if i != 0:  # 第0位不上锁
            lock[i].acquire()

        Task[i].num = i
        Task[i].start()

    print('finish do_train!')


if __name__ == "__main__":
    move_data_from_share_local()
    trans_xml_to_txt()

    lock = []
    Task = [do_train_1(),
            do_train_2(),
            do_train_3(),
            do_train_4(),
            do_train_5()]

    N = len(Task)

    mythreads = []
    mythreads.append(threading.Thread(target=do_train_0))
    mythreads.append(threading.Thread(target=do_train))
    for t in mythreads:
        t.start()
    for t in mythreads:
        t.join()







