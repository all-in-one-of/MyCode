# encoding=utf-8

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

with open(r'C:\Users\HYC\Documents\MyCode\maya\intime\0010000000.json', 'r', encoding='utf-8') as f:
    commodity_info = json.load(f)


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
    time.sleep(0.5)


# 前台开启浏览器模式
def openChrome():
    # 加启动配置
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    # 打开chrome浏览器
    driver = webdriver.Chrome(chrome_options=option)
    return driver


# 授权操作
def operationAuth(driver):
    url = "http://cf.3dintime.com/"
    driver.get(url)
    # 找到输入框并输入查询内容
    userName = driver.find_element_by_name("user")  # 用户
    userName.send_keys("yingtai")
    pwdName = driver.find_element_by_name("pwd")  # 密码
    pwdName.send_keys('YT56894!@#')
    a = driver.find_elements_by_class_name('btn')  # 登陆
    a[0].click()
    b = driver.find_elements_by_xpath('//*[@id="menu-article"]/dt/i[2]')  # 商品管理选单
    b[1].click()
    c = driver.find_elements_by_xpath('//*[@id="menu-article"]/dd/ul/li[1]/a')  # 商品管理
    c[1].click()
    driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[1])  # 选择商品管理frame

    driver.find_element_by_css_selector('body > div > div.cl.pd-5.bg-1.bk-gray.mt-20 > span.l > a').click()  # 添加商品
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    name = driver.find_element_by_id('name')  # 名称
    name.send_keys(commodity_info['商品名称'])
    subname = driver.find_element_by_id('subname')  # 副标题
    subname.send_keys(commodity_info['副标题'])
    parent_id = driver.find_element_by_name('parent_id')  # 选择分类
    time.sleep(0.1)
    Select(parent_id).select_by_visible_text(commodity_info['所属分类'])
    seller_id = driver.find_element_by_name('seller_id')  # 选择商家
    time.sleep(0.1)
    Select(seller_id).select_by_visible_text(commodity_info['所属商家'])
    brand_id = driver.find_element_by_name('brand_id')  # 选择品牌
    time.sleep(0.1)
    Select(brand_id).select_by_visible_text(commodity_info['所属品牌'])
    set_id = driver.find_element_by_name('set_id')  # 选择系列
    time.sleep(0.1)
    Select(set_id).select_by_visible_text(commodity_info['所属系列'])
    sku = driver.find_element_by_name('sku')  # 货号
    sku.send_keys(commodity_info['sku'])
    seller_sku = driver.find_element_by_id("seller_sku")  # 商家sku
    seller_sku.send_keys(commodity_info['商家货号'])
    tech = driver.find_element_by_name('tech')  # 工艺
    tech.send_keys(commodity_info['工艺'])
    material = driver.find_element_by_name('material')  # 材质
    material.send_keys(commodity_info['材质'])
    volume = driver.find_element_by_name('volume')  # 体积
    volume.send_keys('长: %scm  宽: %scm  高: %scm' % (
        commodity_info['商品长宽高'][0], commodity_info['商品长宽高'][2], commodity_info['商品长宽高'][1]))
    style = driver.find_element_by_name('style')  # 风格
    style.send_keys(commodity_info['风格'])
    price = driver.find_element_by_name('price')  # 价格
    price.send_keys(commodity_info['价格'])
    md5 = driver.find_element_by_name('md5')  # MD5
    md5.send_keys(commodity_info['2019-01-12']['MD5码'])
    skin_file = driver.find_element_by_name('skin_file')  # 皮肤包文件
    skin_file.send_keys(commodity_info['2019-01-12']['材质包地址'])
    skin_file_button = driver.find_element_by_css_selector(
        '#form-add-edit > div:nth-child(17) > div.formControls.col-5 > input:nth-child(7)')  # 上传皮肤包按钮
    add = driver.find_element_by_name('add').click()  # 添加规格
    option_name = driver.find_element_by_id('option_name')  # 规格名称
    option_name.send_keys(commodity_info['规格名称'])
    option_price = driver.find_element_by_id('option_price')  # 规格价格
    option_price.send_keys(commodity_info['价格'])
    option_sku = driver.find_element_by_id('option_sku')  # 规格sku
    option_sku.send_keys(commodity_info['sku'])
    option_model_file = driver.find_element_by_name('option_model_file')  # 规格模型文件
    option_model_file.send_keys(commodity_info['2019-01-12']['模型包地址'])
    option_model_file_button = driver.find_element_by_css_selector(
        '#form-add-edit > div:nth-child(18) > div.formControls.col-9 > table > tbody > tr:nth-child(2) > td:nth-child(5) > input.btn.btn-primary.radius')  # 规格模型上传按钮
    option_image_button = driver.find_elements_by_tag_name('label')[18]  # 规格图片上传按钮
    up_image_button = driver.find_elements_by_tag_name('label')[20]  # 图片上传按钮
    status1 = driver.find_elements_by_tag_name('label')[23]  # 上架
    status0 = driver.find_elements_by_tag_name('label')[24]  # 下架
    position = driver.find_element_by_id('position')  # 排序
    position.send_keys(commodity_info['排序'])
    up_image_button.click()
    upfile(commodity_info['2019-01-12']['渲染图片地址'].replace('//', '\\'))
    option_image_button.click()
    upfile(commodity_info['2019-01-12']['渲染图片地址'].replace('//', '\\'))
    skin_file_button.click()
    colseAlert()
    option_model_file_button.click()
    colseAlert()

    # for i in driver.find_elements_by_tag_name('label'):
    #     print(driver.find_elements_by_tag_name('label').index(i), i.text)
    #
    # f[18].click()
    # upfile(r"C:\Users\Intime\Desktop\125017292872085595.png")

    # f[12].send_keys(r"F:\ARKit15 - 副本\AssetBundles\mr01")
    # f[13].click()
    # result = EC.alert_is_present()(driver)
    # while result is False:
    #     time.sleep(1)
    #     result = EC.alert_is_present()(driver)

    # result.accept()

    # f[1].send_keys(r"C:\Users\Intime\Desktop\125017292872085595.png")
    submit = driver.find_element_by_css_selector('#form-add-edit > div:nth-child(22) > div > input')  # 提交
    submit.click()

    # 提交表单
    # driver.find_element_by_xpath("//*[@id='su']").click()
    # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    # print(a)


def modification(driver):
    url = "http://cf.3dintime.com/"
    driver.get(url)
    # 找到输入框并输入查询内容
    userName = driver.find_element_by_name("user")  # 用户
    userName.send_keys("yingtai")
    pwdName = driver.find_element_by_name("pwd")  # 密码
    pwdName.send_keys('YT56894!@#')
    a = driver.find_elements_by_class_name('btn')  # 登陆
    a[0].click()
    b = driver.find_elements_by_xpath('//*[@id="menu-article"]/dt/i[2]')  # 商品管理选单
    b[1].click()
    c = driver.find_elements_by_xpath('//*[@id="menu-article"]/dd/ul/li[1]/a')  # 商品管理
    c[1].click()
    driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[1])  # 选择商品管理frame
    search_name = driver.find_element_by_name('name')  # 按商品名查找
    search_name.send_keys(commodity_info['商品名称'])
    search_button = driver.find_element_by_css_selector('body > div > form > button')  # 搜索按钮
    search_button.click()
    edit_button = driver.find_element_by_css_selector(
        'body > div > div:nth-child(3) > table > tbody > tr > td.td-manage > a:nth-child(1)')  # 编辑按钮
    edit_button.click()
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))


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

    def add_commodity(self, commodity):
        with open(commodity, 'r', encoding='utf-8') as f:
            commodity_info = json.load(f)
        b = driver.find_elements_by_xpath('//*[@id="menu-article"]/dt/i[2]')  # 商品管理选单
        b[1].click()
        c = driver.find_elements_by_xpath('//*[@id="menu-article"]/dd/ul/li[1]/a')  # 商品管理
        c[1].click()
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[1])  # 选择商品管理frame

        driver.find_element_by_css_selector(
            'body > div > div.cl.pd-5.bg-1.bk-gray.mt-20 > span.l > a').click()  # 添加商品
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        self.upload_commodity(commodity_info)

    def revise_commodity(self, commodity):
        with open(commodity, 'r', encoding='utf-8') as f:
            commodity_info = json.load(f)

        b = driver.find_elements_by_xpath('//*[@id="menu-article"]/dt/i[2]')  # 商品管理选单
        b[1].click()
        c = driver.find_elements_by_xpath('//*[@id="menu-article"]/dd/ul/li[1]/a')  # 商品管理
        c[1].click()
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[1])  # 选择商品管理frame
        search_name = driver.find_element_by_name('name')  # 按商品名查找
        search_name.send_keys(commodity_info['商品名称'])
        search_button = driver.find_element_by_css_selector('body > div > form > button')  # 搜索按钮
        search_button.click()
        edit_button = driver.find_element_by_css_selector(
            'body > div > div:nth-child(3) > table > tbody > tr > td.td-manage > a:nth-child(1)')  # 编辑按钮
        edit_button.click()
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        self.upload_commodity(commodity_info)

    def upload_commodity(self, commodity_info, revise=False):
        up_file = []
        up_image = []

        name = driver.find_element_by_id('name')  # 名称
        name.clear()
        name.send_keys(commodity_info['商品名称'])

        subname = driver.find_element_by_id('subname')  # 副标题
        subname.clear()
        subname.send_keys(commodity_info['副标题'])

        parent_id = driver.find_element_by_name('parent_id')  # 选择分类
        time.sleep(0.1)
        Select(parent_id).select_by_visible_text(commodity_info['所属分类'])

        seller_id = driver.find_element_by_name('seller_id')  # 选择商家
        time.sleep(0.1)
        Select(seller_id).select_by_visible_text(commodity_info['所属商家'])

        brand_id = driver.find_element_by_name('brand_id')  # 选择品牌
        time.sleep(0.1)
        Select(brand_id).select_by_visible_text(commodity_info['所属品牌'])

        set_id = driver.find_element_by_name('set_id')  # 选择系列
        time.sleep(0.1)
        Select(set_id).select_by_visible_text(commodity_info['所属系列'])

        sku = driver.find_element_by_name('sku')  # 货号
        sku.clear()
        sku.send_keys(commodity_info['sku'])

        seller_sku = driver.find_element_by_id("seller_sku")  # 商家sku
        seller_sku.clear()
        seller_sku.send_keys(commodity_info['商家货号'])

        tech = driver.find_element_by_name('tech')  # 工艺
        tech.clear()
        tech.send_keys(commodity_info['工艺'])

        material = driver.find_element_by_name('material')  # 材质
        material.clear()
        material.send_keys(commodity_info['材质'])

        volume = driver.find_element_by_name('volume')  # 体积
        volume.clear()
        volume.send_keys('长: %scm  宽: %scm  高: %scm' % (
            commodity_info['商品长宽高'][0], commodity_info['商品长宽高'][2], commodity_info['商品长宽高'][1]))

        style = driver.find_element_by_name('style')  # 风格
        style.clear()
        style.send_keys(commodity_info['风格'])

        price = driver.find_element_by_name('price')  # 价格
        price.clear()
        price.send_keys(commodity_info['价格'])

        md5 = driver.find_element_by_name('md5')  # MD5
        md5.clear()
        md5.send_keys(commodity_info['规格']['2019-01-12']['MD5码'])

        skin_file = driver.find_element_by_name('skin_file')  # 皮肤包文件
        skin_file.send_keys(commodity_info['规格']['2019-01-12']['材质包地址'])

        skin_file_button = driver.find_element_by_css_selector(
            '#form-add-edit > div:nth-child(17) > div.formControls.col-5 > input:nth-child(7)')  # 上传皮肤包按钮

        skin_file_button.click()
        colseAlert()
        # up_file.append(skin_file_button)

        up_image_button = driver.find_element_by_xpath('//*[@id="image"]/div[2]/label')  # 图片上传按钮
        up_image_button.click()
        upfile(commodity_info['商品图片地址'].replace('//', '\\'))

        # up_image.append(up_image_button)

        add = driver.find_element_by_name('add')  # 添加规格
        if revise is False:
            i = 0
            for name, info in commodity_info['规格']['2019-01-12']['模型'].items():
                add.click()

                option_name = driver.find_elements_by_id('option_name')[i]  # 规格名称
                option_name.clear()
                option_name.send_keys(name)

                option_price = driver.find_elements_by_id('option_price')[i]  # 规格价格
                option_price.clear()
                option_price.send_keys(info['价格'])

                option_sku = driver.find_elements_by_id('option_sku')[i]  # 规格sku
                option_sku.clear()
                option_sku.send_keys(info['sku'])

                option_image_button = driver.find_element_by_xpath(
                    '//*[@id="form-add-edit"]/div[18]/div[1]/table/tbody/tr[%s]/td[6]/span/div[2]/label' % (
                                2 + i))  # 图片上传按钮
                # up_image.append(option_image_button)
                option_image_button.click()
                upfile(info['渲染图片地址'].replace('//', '\\'))
                # time.sleep(0.5)
                option_model_file = driver.find_elements_by_name('option_model_file')[i]  # 规格模型文件
                option_model_file.send_keys(info['模型包地址'])
                option_model_file_button = driver.find_element_by_xpath(
                    '//*[@id="form-add-edit"]/div[18]/div[1]/table/tbody/tr[%s]/td[5]/input[3]' % (2 + i))  # 规格模型上传按钮
                option_model_file_button.click()
                colseAlert()

                # up_file.append(option_model_file_button)
                i += 1
        status1 = driver.find_element_by_xpath('//*[@id="form-add-edit"]/div[20]/div[1]/div[1]/label')  # 上架
        status0 = driver.find_element_by_xpath('//*[@id="form-add-edit"]/div[20]/div[1]/div[2]/label')  # 下架

        position = driver.find_element_by_id('position')  # 排序
        position.clear()
        position.send_keys(commodity_info['排序'])

        # for up in up_image:
        #     up.click()
        #     upfile(commodity_info['商品图片地址'].replace('//', '\\'))

        # for up in up_file:
        #     up.click()
        #     colseAlert()


        submit = driver.find_element_by_css_selector('#form-add-edit > div:nth-child(22) > div > input')  # 提交
        submit.click()


# 方法主入口
if __name__ == '__main__':
    # 加启动配置
    driver = openChrome()
    it = InTimeWebUpload()
    it.login()
    it.revise_commodity(r"D:\test\0010000000\0010000000.json")

    # modification(driver)

    # print(commodity_info['2019-01-12']['渲染图片地址'].replace('//','\\'))
