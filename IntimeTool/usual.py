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
import time
import hashlib
import wmi
import zipfile

c = wmi.WMI()
#处理器
def printCPU():
    tmpdict = {}
    tmpdict["CpuCores"] = 0
    for cpu in c.Win32_Processor():
        tmpdict["cpuid"] = cpu.ProcessorId.strip()
        tmpdict["CpuType"] = cpu.Name
        tmpdict['systemName'] = cpu.SystemName
        try:
            tmpdict["CpuCores"] = cpu.NumberOfCores
        except:
            tmpdict["CpuCores"] += 1
        tmpdict["CpuClock"] = cpu.MaxClockSpeed
        tmpdict['DataWidth'] = cpu.DataWidth
    print(tmpdict)
    return  tmpdict

#主板
def printMain_board():
    boards = []
    # print len(c.Win32_BaseBoard()):
    for board_id in c.Win32_BaseBoard():
        tmpmsg = {}
        tmpmsg['UUID'] = board_id.qualifiers['UUID'][1:-1]   #主板UUID,有的主板这部分信息取到为空值，ffffff-ffffff这样的
        tmpmsg['SerialNumber'] = board_id.SerialNumber                #主板序列号
        tmpmsg['Manufacturer'] = board_id.Manufacturer       #主板生产品牌厂家
        tmpmsg['Product'] = board_id.Product                 #主板型号
        boards.append(tmpmsg)
    print(boards)
    return boards

#BIOS
def printBIOS():
    bioss = []
    for bios_id in c.Win32_BIOS():
        tmpmsg = {}
        tmpmsg['BiosCharacteristics'] = bios_id.BiosCharacteristics   #BIOS特征码
        tmpmsg['version'] = bios_id.Version                           #BIOS版本
        tmpmsg['Manufacturer'] = bios_id.Manufacturer.strip()                 #BIOS固件生产厂家
        tmpmsg['ReleaseDate'] = bios_id.ReleaseDate                   #BIOS释放日期
        tmpmsg['SMBIOSBIOSVersion'] = bios_id.SMBIOSBIOSVersion       #系统管理规范版本
        bioss.append(tmpmsg)
    print(bioss)
    return bioss

#硬盘
def printDisk():
    disks = []
    for disk in c.Win32_DiskDrive():
        # print disk.__dict__
        tmpmsg = {}
        tmpmsg['SerialNumber'] = disk.SerialNumber.strip()
        tmpmsg['DeviceID'] = disk.DeviceID
        tmpmsg['Caption'] = disk.Caption
        tmpmsg['Size'] = disk.Size
        tmpmsg['UUID'] = disk.qualifiers['UUID'][1:-1]
        disks.append(tmpmsg)
    for d in disks:
        print(d)
    return disks

#内存
def printPhysicalMemory():
    memorys = []
    for mem in c.Win32_PhysicalMemory():
        tmpmsg = {}
        tmpmsg['UUID'] = mem.qualifiers['UUID'][1:-1]
        tmpmsg['BankLabel'] = mem.BankLabel
        tmpmsg['SerialNumber'] = mem.SerialNumber.strip()
        tmpmsg['ConfiguredClockSpeed'] = mem.ConfiguredClockSpeed
        tmpmsg['Capacity'] = mem.Capacity
        tmpmsg['ConfiguredVoltage'] = mem.ConfiguredVoltage
        memorys.append(tmpmsg)
    for m in memorys:
        print(m)
    return memorys

#电池信息，只有笔记本才会有电池选项
def printBattery():
    isBatterys = False
    for b in c.Win32_Battery():
        isBatterys = True
    return isBatterys

#网卡mac地址：
def printMacAddress():
    macs = []
    for n in  c.Win32_NetworkAdapter():
        mactmp = n.MACAddress
        if mactmp and len(mactmp.strip()) > 5:
            tmpmsg = {}
            tmpmsg['MACAddress'] = n.MACAddress
            tmpmsg['Name'] = n.Name
            tmpmsg['DeviceID'] = n.DeviceID
            tmpmsg['AdapterType'] = n.AdapterType
            tmpmsg['Speed'] = n.Speed
            macs.append(tmpmsg)
    print(macs)
    return macs


def getMd5(file):
    myhash = hashlib.md5()
    with open(file, 'rb')as f:
        b = f.read()
        myhash.update(b)
    return myhash.hexdigest()


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


def customStrftime(t):
    a = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
    return a


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
        json.dump(info, f, ensure_ascii=False, indent=2)


def detectionChinese(text):
    b = re.compile(u'[\u4e00-\u9fa5]+').search(text)
    return b

def refreshMerchantInfo():
    from requests import session, Request
    import re
    from bs4 import BeautifulSoup as bs  # Beautiful Soup是一个可以从HTML或XML文件中提取结构化数据的Python库

    def optionNum():
        sku = []
        skuList = soup.find_all(id='option_sku')
        if len(skuList) == 1:
            sku.append(skuList[0]['value'])
            return sku
        else:

            for i in skuList:
                sku.append(i['value'])
            return sku

    def optionName():
        name = []
        skuList = soup.find_all(id='option_name')
        if len(skuList) == 1:
            name.append(skuList[0]['value'])
            return name
        else:

            for i in skuList:
                name.append(i['value'])
            return name

    def goodsSKU(sku):
        sku = sku[0]
        if len(sku) > 4:
            return sku[:4]
        else:
            return sku

    def goodsName():
        return soup.find(id='name')['value']

    url = "http://cf.3dintime.com/index/index"

    session_req = session()

    postData = {
        "user": "yingtai",
        "pwd": "YT56894!@#"
    }

    # 需要登录的URL
    login_url = "http://cf.3dintime.com/admin_user/public/login/#"
    # PreparedRequest请求预处理
    req = Request(
        'post',
        login_url,
        data=postData,
        headers=dict(referer=login_url)
    )
    prepped = req.prepare()

    # 将处理的请求参数通过session请求对象发送过去
    resp = session_req.send(prepped)
    num = []
    for i in range(7):
        a = session_req.get(
            r'http://cf.3dintime.com/product/product/index?start_at=&end_at=&status=&seller_name=&brand_name=%E8%BD%A9&name=&page=' + '%s' % (
                    i + 1))

        goodslist = re.findall(r'<a href="javascript:layer_full_add_edit(.*?);">编辑</a>', a.text, re.S)

        for goods in goodslist:
            goodsEdit = tuple(eval(goods))[1]

            b = session_req.get(goodsEdit)

            c = b.content

            soup = bs(c, "html.parser")

            goodsinfo = ((goodsName(), goodsSKU(optionNum()), optionName()))
            num.append(goodsinfo)

    print(len(num))
    writeJson(r'C:\Users\Intime\Documents\MyCode\IntimeTool\rdx.json', num)

def zipDir(dirList,output):
    z = zipfile.ZipFile(output,'w',zipfile.ZIP_STORED)
    for dir in dirList:
        z.write(dir)
    z.close()

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
