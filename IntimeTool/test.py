# -*- encoding: utf-8 -*-
"""
@File    : test.py
@Time    : 2019/3/6 19:35
@Author  : Intime
@Software: PyCharm
"""
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
from requests import session, Request, get
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

        goodsinfo = ((goodsName(), goodsSKU(optionNum()),optionName()))
        num.append(goodsinfo)

print(len(num))
writeJson(r'C:\Users\Intime\Documents\MyCode\IntimeTool\rdx.json',num)

# 用BeautifulSoup处理登录之后返回的数据
# soup=bs(resp.content,"html.parser")

# 打印输出
# print(soup.prettify())
