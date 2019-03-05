# -*- encoding: utf-8 -*-
"""
@File    : inputGoodsInfo.py
@Time    : 2019/3/5 13:29
@Author  : Intime
@Software: PyCharm
"""
import os
from pypinyin import *
from usual import *

IntimeInfoJsonPath = r'C:\Users\Intime\Documents\MyCode\InputTool\intimeInfo.json'
IntimeGoodsDir = r'F:\Share\goods'

IntimeInfo = readJson(IntimeInfoJsonPath)
Makers = IntimeInfo['makers']
Merchants = IntimeInfo['merchants']
PAP = IntimeInfo['projectAcceptance']


def createMerchant(merchantName, series):
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
    merchantInfo['series'] = series
    merchantInfo['setList'] = []
    merchantInfo['goodsList'] = []
    merchantJson = os.path.join(merchantDir, '%s.json' % merchant)
    Merchants.append({merchant: merchantName})
    writeJson(IntimeInfoJsonPath, IntimeInfo)
    writeJson(merchantJson, merchantInfo)

    return merchant


def fillGoodsInfo(personnel, merchant, goodsName):
    merchantDir = os.path.join(IntimeGoodsDir, merchant)
    merchantJson = os.path.join(merchantDir, '%s.json' % merchant)
    merchantInfo = readJson(merchantJson)
    goodsInfo = {}
    goodsInfo['name'] = goodsName
    goodsInfo['merchant'] = merchant
    goodsInfo['inputPersonnel'] = personnel


def createSKU(goodsInfo, merchantInfo):
    merchant = goodsInfo['merchant']

    num0_2 = '%03d' % Merchants.index(merchant)

    num3_5 = '%03d' % len(merchantInfo['goodsList'])
    num6_7 = '%02d' % PAP.index(goodsInfo['inputPersonnel'])

    sku = num0_2 + num3_5 + num6_7
    goodsInfo['sku'] = sku
    goodsDir = os.path.join(merchantDir, sku)
    goodsJson = os.path.join(goodsDir, '%s.json' % sku)
    createDirectory(goodsDir)
    writeJson(goodsJson, goodsInfo)
    return sku


class inputTools():
    def __init__(self,merchantName):
        if merchantName not in Merchants:
            self.fillMerchantInfo()
            self.createMerchant(merchantName,self.fillMerchantInfo())

    def fillMerchantInfo(self):
        self.setList = []
        self.series = []
        self.goodList = []
        pass

    def createMerchant(self,merchantName, series):
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
        merchantInfo['series'] = series
        merchantInfo['setList'] = []
        merchantInfo['goodsList'] = []
        merchantJson = os.path.join(merchantDir, '%s.json' % merchant)
        Merchants.append({merchant: merchantName})
        writeJson(IntimeInfoJsonPath, IntimeInfo)
        writeJson(merchantJson, merchantInfo)

        return merchant




if __name__ == '__main__':
    a = createMerchant('双阳红木', [1, 2, 3])
    print(a)
