# -*- encoding: utf-8 -*-
"""
@File    : temp02.py
@Time    : 2019/4/17 19:45
@Author  : Intime
@Software: PyCharm
"""
import cv2

#RGB三通道相同的24位depth 保存为 16位单通道

lab_d = cv2.imread('9.bmp')  # 3通道值相同
b = cv2.split(lab_d)[0]  # 只要1个通道
c = b.astype('uint16')
c *= 256
cv2.imwrite('lab_d16.png', c)