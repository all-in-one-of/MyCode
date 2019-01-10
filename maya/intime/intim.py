# coding=utf-8
import json
import pprint
import ast
import logging
import os

pwd = os.getcwd()

JSONPATH = os.path.join(pwd, '0010000000.json')
TESTJSONPATH = os.path.join(pwd, 'a002.json')


class TestIntmeCommodity(object):

    def __init__(self, info, jsonPath):
        self.jsonPath = jsonPath
        self.info = info
        self.sku = info['sku']
        self.cmName = info['商品名称']
        self.cmModel = info['制作类型']
        self.mdMaker = info['制作人']
        self.hder = info['对接人']
        self.refPhPath = info['参考图地址']
        self.mayaFlPath = info['maya文件地址']
        self.fbxFlPath = info['fbx文件地址']
        self.texFlPath = info['贴图地址']
        self.cmSize = info['商品长宽高']
        self.metaInfo = info['是否有金属配件']
        self.objFlPath = info['obj文件地址']
        self.maxFlPath = info['3dMax地址']

    def skuNumber(self):
        # sku号码
        if self.sku:
            print 'sku:', self.sku
        else:
            logging.warning('sku为空，请联系XX')

    def commodityName(self):
        # 商品名称
        if self.cmName:
            print '商品名称:', self.cmName
        else:
            logging.warning('商品名称为空，请联系XX')

    def commodityModel(self):
        # 制作类型
        if self.cmModel:
            print '制作类型:', self.cmModel
        else:
            print '制作类型: 待定'

    def modelMaker(self, name=None):
        # 制作人
        if self.mdMaker:
            print self.mdMaker
        elif name is None:
            print '等待制作'
        else:
            self.info['制作人'] = name
            print '制作人:', self.info['制作人']
            with open(self.jsonPath, 'w') as f:
                json.dump(self.info, f, indent=2, ensure_ascii=False)

    def header(self):
        # 对接人
        if self.hder:
            print '对接人:', self.hder
        else:
            print '对接人: 联系王老板'

    def referencePhotoPath(self):
        # 参考图地址
        if self.refPhPath:
            print self.refPhPath
        else:
            print '参考图地址: 请联系对接人，等待补全'

    def mayaFilePath(self, path=None):
        # maya文件地址
        if self.mayaFlPath:
            print self.mayaFlPath
        elif path is None:
            print 'maya文件地址: 等待制作'
        else:
            self.info['fbx文件地址'] = path
            print 'fbx文件地址:', path
            with open(self.jsonPath, 'w') as f:
                json.dump(self.info, f, indent=2, ensure_ascii=False)

    def fbxFilePath(self, path=None):
        if self.fbxFlPath and path is None:
            print self.fbxFlPath
        elif path is None:
            print 'fbx文件地址: 等待制作'
        else:
            self.info['fbx文件地址'] = path
            print 'fbx文件地址:', path
            with open(self.jsonPath, 'w') as f:
                json.dump(self.info, f, indent=2, ensure_ascii=False)

    def texFilePath(self, path=None):
        if self.fbxFlPath and path is None:
            print self.fbxFlPath
        elif path is None:
            print '参考图地址: 等待制作'
        else:
            self.info['参考图地址'] = path
            print '参考图地址:', path
            with open(self.jsonPath, 'w') as f:
                json.dump(self.info, f, indent=2, ensure_ascii=False)

    def metalnessInfo(self):
        # 金属信息
        if self.metaInfo:
            print self.metaInfo
        else:
            print '没有金属配件'

    def commoditySize(self):
        if self.cmSize:
            print self.cmSize

        else:
            print '缺少产品信息请联系对接人'

    def objFilePath(self):
        if self.objFlPath():
            print self.objFlPath
        else:
            print "等待制作"

    def maxFilePath(self):
        if self.maxFlPath:
            # os.startfile(self.maxFlPath.decode('utf-8'))
            print '等待打开'

        else:
            print'无模型'


# 读取json文件，转换成字典
def readJson(path):
    with open(path, 'r') as f:
        info = json.load(f)  # 导入json文件
        b = json.dumps(info, encoding="utf-8", ensure_ascii=False)  # 转码成字符串
        c = eval(b)  # 转回字典
    return c  # 返回字典



if __name__ == '__main__':
    commodityInfo = readJson(JSONPATH)

    a = TestIntmeCommodity(commodityInfo, TESTJSONPATH)
    a.commodityName()
    a.skuNumber()
    a.commodityModel()
    a.header()
    a.referencePhotoPath()
    a.mayaFilePath()
    a.fbxFilePath()
    a.modelMaker('王大锤')
    a.texFilePath()
    a.commoditySize()
    a.metalnessInfo()
    a.maxFilePath()
