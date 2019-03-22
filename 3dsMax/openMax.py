# -*- encoding: utf-8 -*-
"""
@File    : openMax.py
@Time    : 2019/3/22 14:45
@Author  : Intime
@Software: PyCharm
"""

import json
import math
import os
import shutil
import datetime
import time
import numpy
import cv2
from win32gui import *
import win32gui
import win32con
from time import sleep
from pykeyboard import PyKeyboard


def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


def openMax():
    kk = PyKeyboard()

    while True:

        win32gui.EnumWindows(get_all_hwnd, 0)

        for h, t in hwnd_title.items():
            if t == "缺少外部文件":
                try:
                    win32gui.PostMessage(h, win32con.WM_CLOSE, 0, 0)
                    print(t)
                except:
                    pass
            elif t == "文件加载: Gamma 和 LUT 设置不匹配":
                try:
                    win32gui.SetForegroundWindow(h)
                    # win32gui.PostMessage(h, win32con.WM_CLOSE, 0, 0)
                    kk.tap_key(kk.enter_key)
                    time.sleep(1)
                except:
                    pass
            elif t == "文件加载: 单位不匹配":
                # win32gui.PostMessage(h, win32con.WM_CLOSE, 0, 0)
                try:
                    win32gui.SetForegroundWindow(h)
                    kk.tap_key(kk.enter_key)
                    time.sleep(1)
                except:
                    pass
            elif t == "V-Ray 警告":
                try:
                    win32gui.SetForegroundWindow(h)
                    kk.tap_key(kk.enter_key)
                    time.sleep(1)
                except:
                    pass
            elif t == '孤立当前选择':
                try:
                    win32gui.SetForegroundWindow(h)
                    kk.tap_key(kk.enter_key)
                    time.sleep(1)
                except:
                    pass

                # win32gui.PostMessage(h, win32con.WM_CLOSE, 0, 0)

            print(h, t)

        time.sleep(1)


hwnd_title = {}

openMax()
