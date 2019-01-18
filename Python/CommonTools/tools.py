# coding=utf-8
import json
import os
import shutil
import datetime
import time
import numpy
import cv2

def findSpecifiedFile(path, suffix=''):
    '''
    查找指定文件
    :param path: 根目录
    :param suffix: 格式，默认是空
    :return: 文件地址列表
    '''
    _file = []
    path = path.decode('utf-8')
    for root, dirs, fils in os.walk(path):
        for file in fils:
            if file.endswith(suffix):
                _file.append(os.path.join(root, file))
    return _file


def copyfile(files, path=None, nummber=1):
    """
    复制文件
    :param files: 文件列表
    :param path: 目标文件夹
    :param nummber: 复制次数
    :return:
    """
    if type(files) is list and path:
        for file in files:
            shutil.copy(file, path)
    elif type(files) is str and path:
        shutil.copy(files, path)
    elif path is None:
        for i in range(nummber):
            for file in files:
                suffix = file.split('.')[1]
                newFile = file.split('.')[0] + '_%s.' % i + suffix
                print newFile
                shutil.copyfile(file, newFile)


def createDirectory(directory):
    '''
    创建路径，如果文件夹不存在，就创建
    :param directory (str): 创建文件夹
    :return:
    '''
    if not os.path.exists(directory):
        os.mkdir(directory)


def readJson(path):
    """
    读取json
    :param path: json文件
    :return: 字典
    """
    with open(path, 'r') as f:
        info = json.load(f)  # 导入json文件
        b = json.dumps(info, encoding="utf-8", ensure_ascii=False)  # 转码成字符串
        c = eval(b)  # 转回字典
    return c  # 返回字典

# print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# path = r"C:\Users\HYC\.anaconda\navigator\images\072618-webinar-AE-FUheroimage-01-3.jpg"
# tpath = r'D:\locaMaya'
#

import cv2

img=cv2.imread(r"D:\HKW\mayacontroller\turtle\bakedTextures\baked_beauty_pPlaneShape1.png")
filename = r"D:\HKW\mayacontroller\turtle\bakedTextures\abc.png"
GrayImage=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

ret,thresh3=cv2.threshold(GrayImage,156,255,cv2.THRESH_TRUNC)
equ = cv2.equalizeHist(thresh3)
cv2.imshow('aaa',thresh3)
cv2.imshow('bbb',equ)
cv2.imwrite(filename, thresh3)
cv2.waitKey(0)
cv2.destroyAllWindows()

from PIL import Image,ImageChops,ImageEnhance,ImageOps

img = Image.open(r"D:\HKW\mayacontroller\turtle\bakedTextures\abc.png")
img = img.convert('L')
img=ImageOps.autocontrast(img)
img.show()
a = []
for i in range(256):
    pixel = img.getpixel((i,2))
    a.append(pixel)

a.sort()
print a[0]