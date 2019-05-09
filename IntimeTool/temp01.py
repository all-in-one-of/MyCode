# -*- encoding: utf-8 -*-
"""
@File    : temp01.py
@Time    : 2019/4/15 14:41
@Author  : Intime
@Software: PyCharm
"""
import datetime

from usual import *

import time

shareDir = r'F:\Share'
outsourcingDir = os.path.join(shareDir, 'outsourcing')
outsourcingJson = os.path.join(outsourcingDir, 'outsourcing.json')

GoodsDir = os.path.join(shareDir, 'goods')

merchant = 'gaojumingzuo'
merchantDir = os.path.join(GoodsDir, merchant)

outsourcingPersonnel = '侯治悦'
outsourcingList = ['00202400', '00206600', '00206800', '00206900', '00207000', '00207200', '00207300']

IntimeInfoJsonPath = r"F:\Share\goods\intimeInfo.json"
IntimeGoodsDir = r'F:\Share\goods'
IntimeInfo = readJson(IntimeInfoJsonPath)


def addOutsourcing(name, goodsList):
    if os.path.exists(outsourcingJson):
        outsourcingInfo = readJson(outsourcingJson)
    else:
        outsourcingInfo = {}
    info = {}
    info['time'] = time.time()
    info['goods'] = goodsList
    outsourcingInfo[name] = info
    writeJson(outsourcingJson, outsourcingInfo)

    for goods in goodsList:
        goodsDir = os.path.join(merchantDir, goods)
        goodsJson = os.path.join(goodsDir, goods + '.json')

        goodsInfo = readJson(goodsJson)

        referImageDir = goodsInfo['refer']

        ma = os.path.join(goodsDir, goods + '.ma')

        Dir = createDirectory(os.path.join(outsourcingDir, goods))

        if os.path.exists(ma):
            shutil.copy(ma, Dir)
        else:
            print(goods)

        try:
            shutil.copytree(referImageDir, Dir + '\\' + 'referImages')
        except:
            print(goods)


if __name__ == '__main__':
    num = len(IntimeInfo['makers']['01']['submitCheck']) + len(IntimeInfo['makers']['02']['submitCheck'])
    print(num)
