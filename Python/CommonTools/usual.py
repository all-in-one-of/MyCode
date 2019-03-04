# -*- encoding: utf-8 -*-
"""
@File    : usual.py
@Time    : 2019/3/2 10:52
@Author  : Intime
@Software: PyCharm
"""
import os
import shutil
import linecache
from PIL import Image, ImageChops, ImageOps, ImageFilter
import json

FilePath = r'D:\newGoods'
RDX = r'F:\Share\2018\rdx'
AssetBundles = r'F:\Share\HHH\ARKit15 - 副本\AssetBundles'


# NewGoods = []


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


def writeJson(path,info):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(info,f,ensure_ascii=False,indent=2)

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


#!/usr/bin/python
# -*- coding: utf-8 -*-
s = {
    "s01": "桑扈·桌",
    "s02": "须臾·茶桌",
    "s03": "流霞明几南宫椅(38CM"
}
# 收藏级
# 优等级
# 实用级
# 一等级
# 具

a = {
    "a001": "参文椅",
    "a002": "参文茶几",
    "a003": "古典卷书搭脑茶几",  # 有金属
    "a004": "江檐椅",  # 有金属
    "a005": "桑扈·椅",
    "a006": "古典卷书搭脑边几",
    "a007": "雀悦长沙发椅",
    "a008": "雀悦短沙发椅",
    "a009": "雀悦平几",  # 有金属
    "a010": "桑扈·案",  # 结构已改
    "a011": "雀悦茶几",  # 有金属
    "a012": "雀悦角几",  # 有金属
    "a013": "若水长沙发椅",
    "a014": "江缘短沙发椅",
    "a015": "若水短沙发椅",
    "a016": "若水平几",  # 有金属
    "a017": "若水茶几",  # 有金属
    "a018": "若水角几",
    "a019": "江缘长沙发椅",
    "a020": "明式餐椅",
    "a021": "简明式餐椅",
    "a022": "清式餐椅",
    "a023": "言炎边柜",  # 有金属
    "a024": "明式圆台（1.76米",
    "a025": "明式圆角画案1.98米",  # 有金属
    "a026": "明式书架",  # 有金属
    "a027": "桑扈柜",  # 材质球命名 #有金属
    "a028": "明式茶桌1.55米",
    "a029": "虚舟茶桌",
    "a030": "虚舟茶凳",
    "a031": "知闲茶桌",
    "a032": "素官帽椅（42CM",
    # "a033": "传统流霞南宫椅(38CM",  # 法线有问题
    "a034": "流霞明几南宫椅(48CM",
    "a035": "禅椅(大",
    "a036": "禅椅(小",
    "a037": "明式圆台1.48米",
    "a038": "明式圆台1.38米",
}
# 具
# 收藏级
# 优等级
# 实用级
# 一等级
b = {
    "b001": "古典卷书搭脑长沙发椅",
    "b002": "古典卷书搭脑短沙发椅",
    "b003": "古典卷书搭脑平几",  # 有金属
    # "b004": "古典卷书搭脑茶几",
    # "b005": "古典卷书搭脑角几",
    "b006": "江缘平几",
    "b007": "江檐茶几",
    "b008": "明式餐桌1.55米",
    "b009": "清式餐桌1.55米",
    "b010": "无尘书柜",  # 有金属
    "b011": "无尘画案（2.18米二抽",  # 有金属
    "b012": "无尘画案（2.38米二抽",  # 有金属
    "b013": "无尘画案（1.78米四抽",  # 有金属
    "b014": "无尘画案（1.98米四抽",  # 有金属
    "b015": "逸兴办公桌（2.18米二抽",  # 有金属
    "b016": "逸兴办公桌（2.38米二抽",  # 有金属
    "b017": "逸兴办公桌（1.78米四抽",  # 有金属
    "b018": "逸兴办公桌（1.98米四抽",  # 有金属
    "b019": "秦韵大办台(3.4米",
    "b020": "秦韵大办台(3.2米",
    "b021": "圈椅茶桌",
    "b022": "疏香茶桌",
    "b023": "疏香长茶凳",
    "b024": "疏香短茶凳",
    "b025": "言炎茶台（3米",
    "b026": "言炎茶台（3.2米",
    "b027": "言炎茶台（5.2米",
    "b028": "圈椅茶几",
    "b029": "圈椅(38CM",
    "b030": "圈椅(48CM",
    "b031": "明式茶几",
    "b032": "素官帽椅（48CM",
    "b033": "四出头官帽椅茶几",
    "b034": "四出头官帽椅",
    "b035": "博古架式茶边柜（右）",
    "b036": "明式三叶博古架1.86米（左）",  # 有金属
    "b037": "明式三叶博古架2米（左）",  # 有金属
    "b038": "明式双抽双门博古架",  # 有金属
    "b039": "明式翘头三联柜",  # 有金属
    "b040": "五抹圆角柜",  # 有金属
    "b041": "无尘（2.6米电视柜）",
    "b042": "无尘（2.2米电视柜）",
    "b043": "听园·柜",  # 有金属
    "b044": "无为·茶柜",  # 有金属
    "B045": "瑾瑜·条案",
    "b046": "纤月·条案",
    # "b047": "桑扈·案",
    "b048": "九格柜",  # 有金属
    "b049": "听园备餐柜",  # 有金属
    "b050": "五斗柜",  # 有金属
    "b051": "明式三叶博古架1.86米(右)",  # 有金属
    "b052": "明式三叶博古架2米（右）",  # 有金属
    "b053": "博古架式茶边柜（左）",
    "b054": "简衣架"
}
# 收藏级
# 优等级
# 实用级
# 一等级
c = {
    # "c001": "江缘炕几",

    "c002": "明式四仙桌",  # 88 78
    "c003": "明式茶水架",
    "c004": "清式茶边架",
    "c005": "明式茶边架",
}
d ={
    "d001": "明式圆角画案2.18米",
    "d002": "明式圆角画案2.38米",
    "d003": "江缘长沙发椅(大)",
    "d004": "逸兴办公桌（1.78米二抽）",
    "d005": "逸兴办公桌（1.98米二抽）",
    "d006": "逸兴办公桌（2.18米四抽）",
    "d007": "逸兴办公桌（2.38米四抽）",

}

# z = readJson(r"D:\newGoods\newGood.json")
#

# a.update(b)
# a.update(c)
# a.update(d)
# a.update(s)
#
# for i in z:
#     a.update({value:key for key, value in i.items()})
# num = 1
# for n in a.values():
#     print('%03d' %num,n)
#     num+=1

for i in os.listdir(r'F:\Share\HHH\荣鼎轩'):
    print(i)