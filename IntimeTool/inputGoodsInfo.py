# -*- encoding: utf-8 -*-
"""
@File    : inputGoodsInfo.py
@Time    : 2019/3/5 13:29
@Author  : Intime
@Software: PyCharm
"""
import os
import time

from pypinyin import *
from IntimeTool.usual import *
import getpass

IntimeInfoJsonPath = r"F:\Share\goods\intimeInfo.json"
IntimeGoodsDir = r'F:\Share\goods'

IntimeInfo = readJson(IntimeInfoJsonPath)
MerchatnsList = IntimeInfo['merchants']
MerchantsDict = IntimeInfo['contrast']
Makers = IntimeInfo['makers']


def initIntimeInfo():
    IntimeInfo = readJson(IntimeInfoJsonPath)
    MerchatnsList = IntimeInfo['merchants']
    MerchantsDict = IntimeInfo['contrast']
    Makers = IntimeInfo['makers']


def createMerchant(merchantName):
    merchantInfo = {}
    if detectionChinese(merchantName):
        merchant = ''
        for i in lazy_pinyin(merchantName):
            merchant += i
    else:
        merchant = merchantName

    merchantDir = os.path.join(IntimeGoodsDir, merchant)
    if os.path.exists(merchantDir):
        merchant = merchant + merchant
    merchantDir = createDirectory(os.path.join(IntimeGoodsDir, merchant))

    merchantInfo['series'] = []
    merchantInfo['brand'] = []
    merchantInfo['setList'] = []
    merchantInfo['goodsList'] = []
    merchantInfo['contrast'] = {}

    merchantJson = os.path.join(merchantDir, '%s.json' % merchant)
    MerchatnsList.append(merchantName)
    MerchantsDict.update({merchantName: merchant})

    writeJson(IntimeInfoJsonPath, IntimeInfo)
    writeJson(merchantJson, merchantInfo)
    initIntimeInfo()
    return merchant


def selectMerchant(merchantName):
    if merchantName in MerchatnsList:
        merchant = MerchantsDict[merchantName]
    else:
        merchant = createMerchant(merchantName)

    return merchant


def fillGoodsInfo(info):
    goodsInfo = {}
    goodsInfo['inputPersonnel'] = info['inputPersonnel']

    goodsInfo['name'] = info['name']

    try:
        goodsInfo['subheading'] = info['subheading']
    except:
        goodsInfo['subheading'] = ''

    goodsInfo['classify'] = info['classify']

    goodsInfo['merchant'] = info['merchant']

    goodsInfo['brand'] = info['brand']

    goodsInfo['series'] = info['series']

    try:
        goodsInfo['goodsImage'] = info['goodsImage']
    except:
        goodsInfo['goodsImage'] = 'lose'
    try:
        goodsInfo['Art.No.'] = info['Art.No.']
    except:
        goodsInfo['Art.No.'] = ''

    try:
        goodsInfo['merchantSKU'] = info['merchantSKU']
    except:
        goodsInfo['merchantSKU'] = ''

    try:
        goodsInfo['craft'] = info['craft']
    except:
        goodsInfo['craft'] = ''

    try:
        goodsInfo['material'] = info['material']
    except:
        goodsInfo['material'] = ''

    try:
        goodsInfo['size'] = info['size']
    except:
        goodsInfo['size'] = [100, 100, 100]

    try:
        goodsInfo['style'] = info['style']
    except:
        goodsInfo['style'] = ''

    try:
        goodsInfo['price'] = info['price']
    except:
        goodsInfo['price'] = 0

    try:
        goodsInfo['refer'] = info['refer']
    except:
        goodsInfo['refer'] = r'F:\Share\original'

    return goodsInfo


def createSKU(goodsInfo):
    merchantName = goodsInfo['merchant']
    merchant = MerchantsDict[merchantName]
    merchantDir = os.path.join(IntimeGoodsDir, merchant)
    merchantJson = os.path.join(merchantDir, '%s.json' % merchant)
    merchantInfo = readJson(merchantJson)
    merchantGoodsList = (merchantInfo['goodsList'])

    num0_2 = '%03d' % MerchatnsList.index(merchantName)

    num3_5 = '%03d' % len(merchantGoodsList)
    num6_7 = goodsInfo['inputPersonnel']

    sku = num0_2 + num3_5 + num6_7

    merchantGoodsList.append(sku)
    merchantInfo['contrast'].update({sku: goodsInfo['name']})
    goodsDir = createDirectory(os.path.join(merchantDir, sku))
    goodsJson = os.path.join(goodsDir, '%s.json' % sku)

    goodsInfo['sku'] = sku
    goodsInfo['makeState'] = 0
    goodsInfo['inputTime'] = time.time()
    if goodsInfo['goodsImage'] != 'lose':
        goodsImage = os.path.join(goodsDir, '%s.jpg' % sku)
        imageSaveAs(goodsInfo['goodsImage'], (1024, 1024), goodsImage)
        goodsInfo['goodsImage'] = goodsImage

    else:
        goodsInfo['goodsImage'] = "C:\\Users\%s\Documents\inputTool\imageLose.jpg" % getpass.getuser()

    writeJson(goodsJson, goodsInfo)
    writeJson(merchantJson, merchantInfo)
    return sku


def allocatingTask(maker, goodsSKU):
    intimeInfo = readJson(IntimeInfoJsonPath)
    merchant = intimeInfo['contrast'][intimeInfo['merchants'][int(goodsSKU[:3])]]
    goodsJsonPath = os.path.join(IntimeGoodsDir, '%s/%s/%s.json' % (merchant, goodsSKU, goodsSKU))
    goodsInfo = readJson(goodsJsonPath)

    intimeInfo['makers'][maker]['unclaimed'].append(goodsSKU)
    goodsInfo['maker'] = maker
    goodsInfo['allocatingTime'] = time.time()

    writeJson(IntimeInfoJsonPath, intimeInfo)
    writeJson(goodsJsonPath, goodsInfo)


def pullTask(maker, goodsSKU):
    intimeInfo = readJson(IntimeInfoJsonPath)
    merchant = intimeInfo['contrast'][intimeInfo['merchants'][int(goodsSKU[:3])]]
    goodsJsonPath = os.path.join(IntimeGoodsDir, '%s/%s/%s.json' % (merchant, goodsSKU, goodsSKU))
    goodsInfo = readJson(goodsJsonPath)

    intimeInfo['makers'][maker]['unclaimed'].remove(goodsSKU)
    intimeInfo['makers'][maker]['undone'].append(goodsSKU)
    goodsInfo['getTime'] = time.time()

    writeJson(IntimeInfoJsonPath, intimeInfo)
    writeJson(goodsJsonPath, goodsInfo)


def beginMake(maker, goodsSKU):
    intimeInfo = readJson(IntimeInfoJsonPath)
    merchant = intimeInfo['contrast'][intimeInfo['merchants'][int(goodsSKU[:3])]]
    goodsJsonPath = os.path.join(IntimeGoodsDir, '%s/%s/%s.json' % (merchant, goodsSKU, goodsSKU))
    goodsInfo = readJson(goodsJsonPath)

    intimeInfo['makers'][maker]['undone'].remove(goodsSKU)
    intimeInfo['makers'][maker]['making'].append(goodsSKU)
    goodsInfo['beginMakeTime'] = time.time()

    writeJson(IntimeInfoJsonPath, intimeInfo)
    writeJson(goodsJsonPath, goodsInfo)


def submitCheck(maker, goodsSKU):
    intimeInfo = readJson(IntimeInfoJsonPath)
    merchant = intimeInfo['contrast'][intimeInfo['merchants'][int(goodsSKU[:3])]]
    goodsJsonPath = os.path.join(IntimeGoodsDir, '%s/%s/%s.json' % (merchant, goodsSKU, goodsSKU))
    goodsInfo = readJson(goodsJsonPath)

    intimeInfo['makers'][maker]['making'].remove(goodsSKU)
    intimeInfo['makers'][maker]['submitCheck'].append(goodsSKU)
    goodsInfo['submitCheckTime'] = time.time()

    writeJson(IntimeInfoJsonPath, intimeInfo)
    writeJson(goodsJsonPath, goodsInfo)


def checkTask(assessor, goodsSKU, isPass):
    intimeInfo = readJson(IntimeInfoJsonPath)
    merchant = intimeInfo['contrast'][intimeInfo['merchants'][int(goodsSKU[:3])]]
    goodsJsonPath = os.path.join(IntimeGoodsDir, '%s/%s/%s.json' % (merchant, goodsSKU, goodsSKU))
    goodsInfo = readJson(goodsJsonPath)

    maker = goodsInfo['maker']
    intimeInfo['makers'][maker]['submitCheck'].remove(goodsSKU)
    if isPass is True:
        intimeInfo['makers'][maker]['waitSubmit'].append(goodsSKU)
    else:
        intimeInfo['makers'][maker]['modification'].append(goodsSKU)

    goodsInfo['checkGoneTime'] = time.time()
    goodsInfo['assessor'] = assessor
    writeJson(IntimeInfoJsonPath, intimeInfo)
    writeJson(goodsJsonPath, goodsInfo)


def doneTask(goodsSKU):
    intimeInfo = readJson(IntimeInfoJsonPath)
    merchant = intimeInfo['contrast'][intimeInfo['merchants'][int(goodsSKU[:3])]]
    goodsJsonPath = os.path.join(IntimeGoodsDir, '%s/%s/%s.json' % (merchant, goodsSKU, goodsSKU))
    goodsInfo = readJson(goodsJsonPath)

    maker = goodsInfo['maker']
    intimeInfo['makers'][maker]['waitSubmit'].remove(goodsSKU)
    intimeInfo['makers'][maker]['done'].append(goodsSKU)

    goodsInfo['doneTime'] = time.time()

    writeJson(IntimeInfoJsonPath, intimeInfo)
    writeJson(goodsJsonPath, goodsInfo)


def fillSpecification(goodsSKU, info):
    specification = {}
    try:
        specification['name'] = info['name']
    except:
        specification['name'] = '默认'
    try:
        specification['price'] = info['price']
    except:
        specification['price'] = 0
    try:
        specification['sku'] = info['sku']
    except:
        specification['sku'] = 0
    try:
        specification['model'] = info['model']
    except:
        specification['model'] = 0
    try:
        specification['photo'] = info['photo']
    except:
        specification['photo'] = 0


def addSpecification(goodsSKU, specifications):
    intimeInfo = readJson(IntimeInfoJsonPath)
    merchant = intimeInfo['contrast'][intimeInfo['merchants'][int(goodsSKU[:3])]]
    goodsJsonPath = os.path.join(IntimeGoodsDir, '%s/%s/%s.json' % (merchant, goodsSKU, goodsSKU))
    goodsInfo = readJson(goodsJsonPath)

    goodsInfo['specifications'] = specifications

    writeJson(goodsJsonPath, goodsInfo)


if __name__ == '__main__':
    merchantName = '高居明作'
    selectMerchant(merchantName)
    merchantINfo = readJson(r"F:\Share\original\gaojumingzuo\gjmz.json")
    merchantINfo = merchantINfo['Done']
    tempList = merchantINfo[:]
    for info in merchantINfo:
        try:
            if info[7] is not None:
                standard = info[7]
            else:
                standard = '默认'
            name = info[1] + '_' + standard
            if '新小南园' in name:
                continue
            if info[3] is not None:
                size = [float(n) for n in info[3].split('*')]
            else:
                size = [100, 100, 100]
            if info[8] is not None:
                classify = info[8]
            else:
                classify = '其他'
            if info[9] is not None:
                series = info[9]
            else:
                series = '其他'
            if info[6] is not None:
                style = info[6]
            else:
                style = '其他'
            if info[5] is not None:
                material = info[5]
            if info[4] is not None:
                artNo = info[4]
            else:
                artNo = '其他'

            imageDir = '%03d' % int(input(name + ': '))

            refer = os.path.join(r'F:\Share\original\gaojumingzuo\image', imageDir)

            goodsInfo = {'inputPersonnel': '00',
                         'name': name,
                         'merchant': merchantName,
                         'classify': classify,
                         'brand': '高居明作',
                         'series': series,
                         'size': size,
                         'style': style,
                         'material': material,
                         'Art.No.': artNo,
                         'refer': refer}

            createSKU(fillGoodsInfo(goodsInfo))
            tempList.remove(info)
        except:
            writeJson('tempList.json', tempList)
            break
