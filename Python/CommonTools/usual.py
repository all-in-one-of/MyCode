# -*- encoding: utf-8 -*-
"""
@File    : usual.py
@Time    : 2019/3/2 10:52
@Author  : Intime
@Software: PyCharm
"""
import math
import os
import re
import shutil
import linecache
from PIL import Image, ImageChops, ImageOps, ImageFilter
import json


def changeTime(allTime):
    day = 24 * 60 * 60
    hour = 60 * 60
    min = 60
    if allTime < 60:
        return "%d sec" % math.ceil(allTime)
    elif allTime > day:
        days = divmod(allTime, day)
        return "%d days, %s" % (int(days[0]), changeTime(days[1]))
    elif allTime > hour:
        hours = divmod(allTime, hour)
        return '%d hours, %s' % (int(hours[0]), changeTime(hours[1]))
    else:
        mins = divmod(allTime, min)
        return "%d mins, %d sec" % (int(mins[0]), math.ceil(mins[1]))


def createDirectory(directory):
    '''
    创建路径，如果文件夹不存在，就创建
    :param directory (str): 创建文件夹
    :return:
    '''
    if not os.path.exists(directory):
        os.mkdir(directory)
    return directory


def findSpecifiedFile(path, suffix=''):
    '''
    查找指定文件
    :param path: 根目录
    :param suffix: 格式，默认是空
    :return: 文件地址列表
    '''
    _file = []
    for root, dirs, fils in os.walk(path):
        for file in fils:
            if file.endswith(suffix):
                _file.append(os.path.join(root, file))
    return _file


def baseNameForPath(path, suffix=True):
    '''
    获取路径文件名
    :param path: 文件路径
    :param suffix: 是否需要后缀
    :return: 文件名
    '''
    name = os.path.basename(path)
    if suffix:
        return name

    else:
        name, b = os.path.splitext(name)
        return name


def imageSaveAs(oPath, size, tPath=None, suffix=None):
    if tPath is None and suffix is None:
        tPath = oPath
    elif suffix is True:
        tPath = oPath.replace(oPath.split('.')[-1], suffix)
    im = Image.open(oPath)
    im = im.resize(size, Image.ANTIALIAS)
    im.save(tPath)
    return im


def readJson(path):
    """
    读取json
    :param path: json文件
    :return: 字典
    """
    with open(path, 'r', encoding='utf-8') as f:
        _info = json.load(f)  # 导入json文件
        # b = json.dumps(info, encoding="utf-8", ensure_ascii=False)  # 转码成字符串
        # c = eval(b)  # 转回字典
    return _info  # 返回字典


def writeJson(jsonPath, info):
    with open(jsonPath, 'w', encoding='utf-8') as f:
        json.dump(info,f,ensure_ascii=False,indent=2)


def detectionChinese(text):
    b = re.compile(u'[\u4e00-\u9fa5]+').search(text)
    return b
# # with open(os.path.join(FilePath,'newGoods.json'),'w',encoding='utf-8') as f:
# for dir in os.listdir(FilePath):
#     a = {}
#
#     if os.path.isdir(os.path.join(FilePath, dir)):
#         for file in os.listdir(os.path.join(FilePath, dir)):
#             if file.endswith('jpg'):
#                 a[file.split('.')[0]] = dir
#                 NewGoods.append(a)
# #     json.dump(NewGoods,f,ensure_ascii=False,indent=2)
#
#


# for i in ['z026','z027']:
#     directory = os.path.join(FilePath, i)
#     if os.path.isdir(directory):
#         jsonFile = os.path.join(directory, '%s.json' % i)
#         goodsInfo = readJson(jsonFile)
#
#         a = {}
#         b = {}
#         c = {}
#
#         d = {}
#         e = {}
#         f = {}
#         g = {}
#
#         a['finally'] = b
#
#         c['收藏级'] = d
#         c['优等级'] = e
#         c['实用级'] = f
#         c['一等级'] = g
#
#         shutil.copy(os.path.join(AssetBundles, '%s' % i), directory)
#         d['模型包地址'] = os.path.join(directory, '%s' % i)
#         d['价格'] = 0
#         d['sku'] = '%s' % i
#         d['渲染图片地址'] = os.path.join(directory, '%s.jpg' % i)
#
#         shutil.copy(os.path.join(AssetBundles, '%s1' % i), directory)
#         e['模型包地址'] = os.path.join(directory, '%s1' % i)
#         e['价格'] = 0
#         e['sku'] = '%s1' % i
#         e['渲染图片地址'] = os.path.join(directory, '%s.jpg' % i)
#
#         shutil.copy(os.path.join(AssetBundles, '%s2' % i), directory)
#         f['模型包地址'] = os.path.join(directory, '%s2' % i)
#         f['价格'] = 0
#         f['sku'] = '%s2' % i
#         f['渲染图片地址'] = os.path.join(directory, '%s.jpg' % i)
#
#         shutil.copy(os.path.join(AssetBundles, '%s3' % i), directory)
#         g['模型包地址'] = os.path.join(directory, '%s3' % i)
#         g['价格'] = 0
#         g['sku'] = '%s3' % i
#         g['渲染图片地址'] = os.path.join(directory, '%s.jpg' % i)
#
#         shutil.copy(os.path.join(AssetBundles, 'm%s' % i), directory)
#         b['材质包地址'] = os.path.join(directory, 'm%s' % i)
#
#         hashCode = linecache.getline(os.path.join(AssetBundles, 'm%s.manifest' % i), 6).split(' ')[-1].replace('\n', '')
#         b['MD5码'] = hashCode
#         b['模型'] = c
#
#         goodsInfo['规格'] = a
#         goodsInfo['所属商家'] = "荣鼎轩红木"
#         goodsInfo['所属品牌'] = '荣鼎轩'
#         goodsInfo['所属分类'] = '客厅'
#         goodsInfo['所属系列'] = '其他'
#         goodsInfo['商家货号'] = ''
#         goodsInfo['商品长宽高'] = [1, 1, 1]
#         goodsInfo['副标题'] = ''
#         goodsInfo['价格'] = 0
#         goodsInfo['工艺'] = '榫卯'
#         goodsInfo['材质'] = '紫光檀'
#         goodsInfo['风格'] = '新中式'
#         goodsInfo['商品图片地址'] = os.path.join(directory, '%s.jpg' % i)
#         goodsInfo['排序'] = 100
#
#         with open(jsonFile, 'w', encoding='utf-8')as f:
#             json.dump(goodsInfo, f, ensure_ascii=False, indent=2)
#
#     # break

