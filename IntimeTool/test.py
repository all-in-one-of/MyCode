# -*- encoding: utf-8 -*-
"""
@File    : test.py
@Time    : 2019/3/6 19:35
@Author  : Intime
@Software: PyCharm
"""
import subprocess

from IntimeTool.usual import *

# ab = r"F:\Share\createAssetBundels\AssetBundles"
# merchantPath = r"F:\Share\goods\yingtaikeji"
# merchantInfo = readJson(os.path.join(merchantPath, 'yingtaikeji.json'))
#
# for i in merchantInfo['goodsList']:
#     goodsJson = os.path.join(merchantPath, '%s\\%s.json' % (i, i))
#     goodsInfo = readJson(goodsJson)
#
#     goodsImage = os.path.join(merchantPath, '%s\\%s.jpg' % (i, i))
#     goodsInfo['goodsImage'] = goodsImage
#
#     skinMD5 = getMd5(goodsImage)
#     goodsInfo['skinMD5'] = skinMD5
#
#     skinPackage = os.path.join(ab, 'm%s' % i)
#     goodsInfo['skinPackage']=skinPackage
#
#     specification = {}
#     specification['name']='默认'
#     specification['price']=0
#     specification['sku']='s'+i
#     specification['goodsImage'] = goodsImage
#
#     model = os.path.join(ab,'s'+i)
#     specification['model']=model
#     goodsInfo['specifications']=[]
#
#     goodsInfo['specifications'].append(specification)
#     writeJson(goodsJson,goodsInfo)


from subprocess import Popen, PIPE, STDOUT
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
command = r'SimplygonBatch --Input F:\Share\simplygon\inputDir --Output F:\Share\simplygon\outputDir --Spl F:\Share\simplygon\splDir --Temp F:\Share\simplygon\temp --Verbose --OutputFileFormat .fbx'
p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
output, errors = p.communicate()

if errors:
    print(errors)

print(output.decode(encoding='gbk'))
