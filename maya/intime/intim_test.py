# coding=utf-8
import json
import pprint
import ast
import logging

PATH = r'C:\Users\Intime\Documents\MyCode\maya\intime\a001.json'


class TestIntmeCommodity(object):

    def __init__(self, info):
        self.info = info
        self.sku = info['sku']
        self.cmName = info['名称']
        self.cmModel = info['制作类型']
        self.mdMaker = info['制作人']
        self.hder = info['对接人']
        self.refPhPath = info['参考图地址']
        self.mayaFlPath = info['maya文件地址']


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

    def commodityModel(self, info):
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
            with open(r'C:\Users\Intime\Documents\MyCode\maya\intime\a002.json', 'w') as f:
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

    def mayaFilePath(self,path=None):
        # maya文件地址
        if self.mayaFlPath:
            print self.mayaFlPath
        elif path is None:
            print 'maya文件地址: 等待制作'
        else:
            self.info['maya文件地址'] = path
            print 'maya文件地址:', path
            with open(r'C:\Users\Intime\Documents\MyCode\maya\intime\a002.json', 'w') as f:
                json.dump(self.info, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    with open(PATH, 'r') as f:
        info = json.load(f)
        b = json.dumps(info, encoding="utf-8", ensure_ascii=False)
        c = b.encode('utf-8')
        d = eval(c)

    a = TestIntmeCommodity(d)
    a.commodityName()
    a.skuNumber()
    a.commodityModel(d)
    a.modelMaker('王大锤')
    a.header()
    a.referencePhotoPath()
    a.mayaFilePath()
