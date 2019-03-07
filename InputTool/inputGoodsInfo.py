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
from usual import *
import getpass

IntimeInfoJsonPath = r'C:\Users\Intime\Documents\MyCode\InputTool\intimeInfo.json'
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

    intimeInfo['makers'][maker]['待领取'].append(goodsSKU)
    goodsInfo['maker'] = maker
    goodsInfo['allocatingTime'] = time.time()

    writeJson(IntimeInfoJsonPath, intimeInfo)
    writeJson(goodsJsonPath, goodsInfo)


def pullTask(maker, goodsSKU):
    intimeInfo = readJson(IntimeInfoJsonPath)
    merchant = intimeInfo['contrast'][intimeInfo['merchants'][int(goodsSKU[:3])]]
    goodsJsonPath = os.path.join(IntimeGoodsDir, '%s/%s/%s.json' % (merchant, goodsSKU, goodsSKU))
    goodsInfo = readJson(goodsJsonPath)

    intimeInfo['makers'][maker]['待领取'].remove(goodsSKU)
    intimeInfo['makers'][maker]['未完成'].append(goodsSKU)
    goodsInfo['getTime'] = time.time()

    writeJson(IntimeInfoJsonPath, intimeInfo)
    writeJson(goodsJsonPath, goodsInfo)


def beginMake(maker, goodsSKU):
    intimeInfo = readJson(IntimeInfoJsonPath)
    merchant = intimeInfo['contrast'][intimeInfo['merchants'][int(goodsSKU[:3])]]
    goodsJsonPath = os.path.join(IntimeGoodsDir, '%s/%s/%s.json' % (merchant, goodsSKU, goodsSKU))
    goodsInfo = readJson(goodsJsonPath)

    intimeInfo['makers'][maker]['未完成'].remove(goodsSKU)
    intimeInfo['makers'][maker]['正在制作'].append(goodsSKU)
    goodsInfo['beginMakeTime'] = time.time()

    writeJson(IntimeInfoJsonPath, intimeInfo)
    writeJson(goodsJsonPath, goodsInfo)


def waitFowReview(maker, goodsSKU):
    intimeInfo = readJson(IntimeInfoJsonPath)
    merchant = intimeInfo['contrast'][intimeInfo['merchants'][int(goodsSKU[:3])]]
    goodsJsonPath = os.path.join(IntimeGoodsDir, '%s/%s/%s.json' % (merchant, goodsSKU, goodsSKU))
    goodsInfo = readJson(goodsJsonPath)

    intimeInfo['makers'][maker]['正在制作'].remove(goodsSKU)
    intimeInfo['makers'][maker]['等待审核'].append(goodsSKU)
    goodsInfo['beginMakeTime'] = time.time()

    writeJson(IntimeInfoJsonPath, intimeInfo)
    writeJson(goodsJsonPath, goodsInfo)


if __name__ == '__main__':
    # merchantName = '映泰科技'
    # selectMerchant(merchantName)
    # goodsInfo = {'inputPersonnel': '00',
    #              'name': '测评（双洋 | 简悟角几）',
    #              'merchant': '映泰科技',
    #              'classify': '其他',
    #              'brand': '映像家居',
    #              'series': '公共素材'}
    # createSKU(fillGoodsInfo(goodsInfo))
    #

   allocatingTask('01', '00000200')
