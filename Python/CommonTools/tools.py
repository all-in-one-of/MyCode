# coding=utf-8
import json
import os
import shutil
import datetime
import time


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
    if path:
        for file in files:
            shutil.copy(file, path)
    if path is None:
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