# -*- encoding: utf-8 -*-
"""
@File    : test.py
@Time    : 2019/3/6 19:35
@Author  : Intime
@Software: PyCharm
"""
from IntimeTool.usual import *

ab = r"F:\Share\createAssetBundels\AssetBundles"
merchantPath = r"F:\Share\goods\yingtaikeji"
merchantInfo = readJson(os.path.join(merchantPath, 'yingtaikeji.json'))

for i in merchantInfo['goodsList']:
    goodsJson = os.path.join(merchantPath, '%s\\%s.json' % (i, i))
    goodsInfo = readJson(goodsJson)

    goodsImage = os.path.join(merchantPath, '%s\\%s.jpg' % (i, i))
    goodsInfo['goodsImage'] = goodsImage

    skinMD5 = getMd5(goodsImage)
    goodsInfo['skinMD5'] = skinMD5

    skinPackage = os.path.join(ab, 'm%s' % i)
    goodsInfo['skinPackage']=skinPackage

    specification = {}
    specification['name']='默认'
    specification['price']=0
    specification['sku']='s'+i
    specification['goodsImage'] = goodsImage

    model = os.path.join(ab,'s'+i)
    specification['model']=model
    goodsInfo['specifications']=[]

    goodsInfo['specifications'].append(specification)
    writeJson(goodsJson,goodsInfo)
