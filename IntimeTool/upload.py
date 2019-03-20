# encoding=utf-8
import math
import os

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import win32gui
import win32con
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import json
from IntimeTool.usual import *


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


def findSpecifiedFile(path, suffix=''):
    """
    查找指定文件
    :param path: 根目录
    :param suffix: 格式，默认是空
    :return: 文件地址列表
    """
    _file = []
    for root, dirs, fils in os.walk(path):
        for file in fils:
            if file.endswith(suffix):
                _file.append(os.path.join(root, file))
    return _file


def colseAlert():
    result = EC.alert_is_present()(driver)
    while result is False:
        time.sleep(1)
        result = EC.alert_is_present()(driver)

    result.accept()


def upfile(file):
    time.sleep(0.5)

    kk = PyKeyboard()
    time.sleep(0.5)

    kk.type_string(file)

    time.sleep(0.5)

    kk.tap_key(kk.enter_key)
    time.sleep(1)


# 前台开启浏览器模式
def openChrome():
    # 加启动配置
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    # 打开chrome浏览器
    driver = webdriver.Chrome(chrome_options=option)
    return driver


# 授权操作


class InTimeWebUpload():

    def login(self):
        url = "http://cf.3dintime.com/"
        driver.get(url)
        userName = driver.find_element_by_name("user")  # 用户
        userName.send_keys("yingtai")
        pwdName = driver.find_element_by_name("pwd")  # 密码
        pwdName.send_keys('YT56894!@#')
        login_button = driver.find_element_by_css_selector(
            '#loginform > form > div:nth-child(3) > div > input.btn.btn-success.radius.size-L')  # 登陆
        login_button.click()

    def initGoodsInfo(self, goodsInfo):
        self.name = goodsInfo['name']
        self.subheading = goodsInfo['subheading']
        self.classify = goodsInfo['classify']
        self.merchant = goodsInfo['merchant']
        self.brand = goodsInfo['brand']
        self.series = goodsInfo['series']
        self.goodsImage = goodsInfo['goodsImage']
        self.ArtNo = goodsInfo['Art.No.']
        self.merchantSKU = goodsInfo['merchantSKU']
        self.craft = goodsInfo['craft']
        self.material = goodsInfo['material']
        self.size = tuple(goodsInfo['size'])
        self.style = goodsInfo['style']
        self.price = goodsInfo['price']
        self.sku = goodsInfo['sku']
        self.skinMD5 = goodsInfo['skinMD5']
        self.skinPackage = goodsInfo['skinPackage']
        self.specifications = goodsInfo['specifications']
        self.sort = goodsInfo['sort']

    def add_commodity(self):
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[1])  # 选择商品管理frame

        driver.find_element_by_css_selector(
            'body > div > div.cl.pd-5.bg-1.bk-gray.mt-20 > span.l > a').click()  # 添加商品
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))

        self.upload_commodity()

    def revise_commodity(self):
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[1])  # 选择商品管理frame
        search_name = driver.find_element_by_name('name')  # 按商品名查找
        search_name.clear()
        search_name.send_keys(self.name)
        search_button = driver.find_element_by_css_selector('body > div > form > button')  # 搜索按钮
        search_button.click()
        edit_button = driver.find_element_by_css_selector(
            'body > div > div:nth-child(3) > table > tbody > tr > td.td-manage > a:nth-child(1)')  # 编辑按钮
        edit_button.click()
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        self.upSkinPackage()
        self.submit()

    def upload_commodity(self):
        '''
        上传商品
        :return:
        '''
        self.upSubheading()
        self.selectClassify()
        self.selectMerchant()
        self.selectBrand()
        self.selectSeries()
        self.upMerchantSKU()
        self.upCraft()
        self.upMaterial()
        self.upSize()
        self.upStyle()
        self.upPrice()
        self.upMD5()
        self.upGoodsImage()
        self.upSkinPackage()
        self.up_option()
        self.putaway()
        self.upSort()
        self.submit()

    def up_option(self):
        add = driver.find_element_by_name('add')  # 添加规格
        i = 0
        for specification in self.specifications:
            add.click()

            option_name = driver.find_elements_by_id('option_name')[i]  # 规格名称
            option_name.clear()
            option_name.send_keys(specification['name'])

            option_price = driver.find_elements_by_id('option_price')[i]  # 规格价格
            option_price.clear()
            option_price.send_keys(specification['price'])

            option_sku = driver.find_elements_by_id('option_sku')[i]  # 规格sku
            option_sku.clear()
            option_sku.send_keys(specification['sku'])

            option_image = driver.find_elements_by_name('option_image_path')[i]  # 图片文件
            option_image.send_keys(specification['goodsImage'])

            option_image_button = driver.find_elements_by_name('upload_option_image')[i]  # # 图片按钮
            option_image_button.click()
            colseAlert()

            # time.sleep(0.5)
            option_model_file = driver.find_elements_by_name('option_model_file')[i]  # 规格模型文件
            option_model_file.send_keys(specification['model'])
            option_model_file_button = driver.find_elements_by_name('upload_option_model')[i]  # 规格模型上传按钮
            option_model_file_button.click()
            colseAlert()
            # up_file.append(option_model_file_button)
            i += 1

    def upSkinPackage(self):
        '''
        上传皮肤包
        :return:
        '''
        skin_file = driver.find_element_by_name('skin_file')  # 皮肤包文件
        skin_file.send_keys(self.skinPackage)

        skin_file_button = driver.find_element_by_name('upload_model')  # 上传皮肤包按钮

        skin_file_button.click()
        colseAlert()

    def submit(self):
        '''
        上传提交
        :return:
        '''
        submit = driver.find_element_by_css_selector('#form-add-edit > div:nth-child(23) > div > input')  # 提交
        print(self.sku, self.name)

        submit.click()

        time.sleep(4)

    def upGoodsImage(self):
        '''
        上传商品图片
        :return:
        '''

        up_image = driver.find_element_by_name('image_path')  # 图片文件

        up_image.send_keys(self.goodsImage)

        up_image_button = driver.find_element_by_name('upload_image')  # 图片上传按钮

        up_image_button.click()
        colseAlert()

    def upMD5(self):
        '''
        上传MD5码
        :return:
        '''
        md5 = driver.find_element_by_name('md5')  # MD5
        md5.clear()
        md5.send_keys(self.skinMD5)

    def upPrice(self):
        '''
        上传价格
        :return:
        '''
        price = driver.find_element_by_name('price')  # 价格
        price.clear()
        price.send_keys(self.price)

    def upStyle(self):
        '''
        上传风格
        :return:
        '''
        style = driver.find_element_by_name('style')  # 风格
        style.clear()
        style.send_keys(self.style)

    def upSize(self):
        '''
        上传体积
        :return:
        '''

        volume = driver.find_element_by_name('volume')  # 体积
        volume.clear()
        volume.send_keys('长: %scm  宽: %scm  高: %scm' % self.size)

    def upMaterial(self):
        '''
        上传材质
        :return:
        '''
        material = driver.find_element_by_name('material')  # 材质
        material.clear()
        material.send_keys(self.material)

    def upCraft(self):
        '''
        上传工艺
        :return:
        '''
        tech = driver.find_element_by_name('tech')  # 工艺
        tech.clear()
        tech.send_keys(self.craft)

    def upMerchantSKU(self):
        '''
        上传商家sku
        :return:
        '''
        seller_sku = driver.find_element_by_id("seller_sku")  # 商家sku
        seller_sku.clear()
        seller_sku.send_keys(self.merchantSKU)

    def upSKU(self):
        '''
        上传货号
        :return:
        '''
        sku = driver.find_element_by_name('sku')  # 货号
        sku.clear()
        sku.send_keys(self.sku)

    def selectSeries(self):
        '''
        选择系列
        :return:
        '''
        set_id = driver.find_element_by_name('set_id')  # 选择系列
        time.sleep(0.1)
        Select(set_id).select_by_visible_text(self.series)

    def selectBrand(self):
        '''
        选择品牌
        :return:
        '''
        brand_id = driver.find_element_by_name('brand_id')  # 选择品牌
        time.sleep(0.1)
        Select(brand_id).select_by_visible_text(self.brand)

    def selectMerchant(self):
        '''
        选择商家
        :return:
        '''
        seller_id = driver.find_element_by_name('seller_id')  # 选择商家
        time.sleep(0.1)
        Select(seller_id).select_by_visible_text(self.merchant)

    def selectClassify(self):
        '''
        选择分类
        :return:
        '''
        parent_id = driver.find_element_by_name('parent_id')  # 选择分类
        time.sleep(0.1)
        Select(parent_id).select_by_visible_text(self.classify)

    def upSubheading(self):
        '''
        上传副标题
        :return:
        '''
        subname = driver.find_element_by_id('subname')  # 副标题
        subname.clear()
        subname.send_keys(self.subheading)

    def upName(self):
        '''
        上传名称
        :return:
        '''
        name = driver.find_element_by_id('name')  # 名称
        name.clear()
        name.send_keys(self.name)

    def goodsManage(self):
        '''
        商品管理
        :return:
        '''
        b = driver.find_elements_by_xpath('//*[@id="menu-article"]/dt/i[2]')  # 商品管理选单
        b[1].click()

        c = driver.find_elements_by_xpath('//*[@id="menu-article"]/dd/ul/li[1]/a')  # 商品管理
        c[1].click()

    def upSort(self):
        '''
        上传排序
        :return:
        '''
        position = driver.find_element_by_id('position')  # 排序
        position.clear()
        position.send_keys(self.sort)

    def putaway(self, putaway=True):
        if putaway:
            status1 = driver.find_element_by_css_selector(
                '#form-add-edit > div:nth-child(21) > div.formControls.col-5.skin-minimal > div:nth-child(1) > div')  # 上架
            status1.click()

        else:
            status0 = driver.find_element_by_xpath('//*[@id="form-add-edit"]/div[21]/div[1]/div[2]/label')  # 下架
            status0.click()


# 方法主入口
if __name__ == '__main__':

    merchantPath = r"F:\Share\goods\yingtaikeji"
    merchantInfo = readJson(os.path.join(merchantPath, 'yingtaikeji.json'))

    start = time.time()
    # 加启动配置
    driver = openChrome()
    it = InTimeWebUpload()
    it.login()

    for i in merchantInfo['goodsList']:
        goodsJson = os.path.join(merchantPath, '%s/%s.json' % (i, i))
        goodsInfo = readJson(goodsJson)

        it.initGoodsInfo(goodsInfo)
        it.revise_commodity()
    end = time.time()
    print(changeTime(end - start))

