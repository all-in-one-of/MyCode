import json
# encoding=utf-8
import math
import os
# import shutil
# import time
#
# import win32con
#
# import win32gui
# from pykeyboard import PyKeyboard
# from pymouse import PyMouse
# from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.select import Select
#

# def findSpecifiedFile(path, suffix=''):
#     '''
#     查找指定文件
#     :param path: 根目录
#     :param suffix: 格式，默认是空
#     :return: 文件地址列表
#     '''
#     _file = []
#     for root, dirs, fils in os.walk(path):
#         for file in fils:
#             if file.endswith(suffix):
#                 _file.append(os.path.join(root, file))
#     return _file
#
#
# a = findSpecifiedFile(r'F:\Share\2018\rdx', 'json')
# # a = findSpecifiedFile(r'C:\Users\Intime\Documents\MyCode\maya\intime', 'json')
#
# for i in a:
#     # with open(i, 'r',encoding='utf-8')as f:
#     #     _info = json.load(f)
#     # with open(i, 'w')as f:
#     #     json.dump(_info, f,indent=2, ensure_ascii=False)
#     with open(i,'r',encoding='utf-8') as f:
#         _info = json.load(f)
#         _info[u'制作状态'] = 4
#
#         # json.dumps(_info,indent=2,ensure_ascii=False)
#     with open(i,'w',encoding='utf-8')as f:
#         json.dump(_info, f,indent=2,ensure_ascii=False)
#     print(i)
#
#
#
#

#
# def changeTime(allTime):
#     day = 24 * 60 * 60
#     hour = 60 * 60
#     min = 60
#     if allTime < 60:
#         return "%d sec" % math.ceil(allTime)
#     elif allTime > day:
#         days = divmod(allTime, day)
#         return "%d days, %s" % (int(days[0]), changeTime(days[1]))
#     elif allTime > hour:
#         hours = divmod(allTime, hour)
#         return '%d hours, %s' % (int(hours[0]), changeTime(hours[1]))
#     else:
#         mins = divmod(allTime, min)
#         return "%d mins, %d sec" % (int(mins[0]), math.ceil(mins[1]))
#
#
# def findSpecifiedFile(path, suffix=''):
#     '''
#     查找指定文件
#     :param path: 根目录
#     :param suffix: 格式，默认是空
#     :return: 文件地址列表
#     '''
#     _file = []
#     for root, dirs, files in os.walk(path):
#         for file in files:
#             if file.endswith(suffix):
#                 _file.append(os.path.join(root, file))
#     return _file
#
#
# def colseAlert():
#     result = EC.alert_is_present()(driver)
#     while result is False:
#         time.sleep(1)
#         result = EC.alert_is_present()(driver)
#
#     result.accept()
#
#
# def upfile(file):
#     time.sleep(0.5)
#
#     kk = PyKeyboard()
#     time.sleep(0.5)
#
#     kk.type_string(file)
#
#     time.sleep(0.5)
#
#     kk.tap_key(kk.enter_key)
#     time.sleep(1)
#
#
# # 前台开启浏览器模式
# def openChrome():
#     # 加启动配置
#     option = webdriver.ChromeOptions()
#     option.add_argument('disable-infobars')
#     # 打开chrome浏览器
#     driver = webdriver.Chrome(chrome_options=option)
#     return driver
#
#
# # 授权操作
#
#
# class InTimeWebUpload():
#
#     def login(self):
#         url = "http://cf.3dintime.com/"
#         driver.get(url)
#         userName = driver.find_element_by_name("user")  # 用户
#         userName.send_keys("yingtai")
#         pwdName = driver.find_element_by_name("pwd")  # 密码
#         pwdName.send_keys('YT56894!@#')
#         login_button = driver.find_element_by_css_selector(
#             '#loginform > form > div:nth-child(3) > div > input.btn.btn-success.radius.size-L')  # 登陆
#         login_button.click()
#
#     def add_commodity(self, commodity):
#         with open(commodity, 'r', encoding='utf-8') as f:
#             commodity_info = json.load(f)
#         b = driver.find_elements_by_xpath('//*[@id="menu-article"]/dt/i[2]')  # 商品管理选单
#         b[1].click()
#         c = driver.find_elements_by_xpath('//*[@id="menu-article"]/dd/ul/li[1]/a')  # 商品管理
#         c[1].click()
#         driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[1])  # 选择商品管理frame
#
#         driver.find_element_by_css_selector(
#             'body > div > div.cl.pd-5.bg-1.bk-gray.mt-20 > span.l > a').click()  # 添加商品
#         driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
#         self.upload_commodity(commodity_info)
#
#     def revise_commodity(self, commodity, revise=True):
#         with open(commodity, 'r', encoding='utf-8') as f:
#             commodity_info = json.load(f)
#
#         b = driver.find_elements_by_xpath('//*[@id="menu-article"]/dt/i[2]')  # 商品管理选单
#         b[1].click()
#         c = driver.find_elements_by_xpath('//*[@id="menu-article"]/dd/ul/li[1]/a')  # 商品管理
#         c[1].click()
#         driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[1])  # 选择商品管理frame
#         search_name = driver.find_element_by_name('name')  # 按商品名查找
#         search_name.send_keys(commodity_info['商品名称'])
#         search_button = driver.find_element_by_css_selector('body > div > form > button')  # 搜索按钮
#         search_button.click()
#         edit_button = driver.find_element_by_css_selector(
#             'body > div > div:nth-child(3) > table > tbody > tr > td.td-manage > a:nth-child(1)')  # 编辑按钮
#         edit_button.click()
#         driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
#         self.upload_commodity(commodity_info, revise)
#
#     def upload_commodity(self, commodity_info, revise=False):
#         up_file = []
#         up_image = []
#
#         name = driver.find_element_by_id('name')  # 名称
#         name.clear()
#         name.send_keys(commodity_info['商品名称'])
#
#         subname = driver.find_element_by_id('subname')  # 副标题
#         subname.clear()
#         subname.send_keys(commodity_info['副标题'])
#
#         parent_id = driver.find_element_by_name('parent_id')  # 选择分类
#         time.sleep(0.1)
#         Select(parent_id).select_by_visible_text(commodity_info['所属分类'])
#
#         seller_id = driver.find_element_by_name('seller_id')  # 选择商家
#         time.sleep(0.1)
#         Select(seller_id).select_by_visible_text(commodity_info['所属商家'])
#
#         brand_id = driver.find_element_by_name('brand_id')  # 选择品牌
#         time.sleep(0.1)
#         Select(brand_id).select_by_visible_text(commodity_info['所属品牌'])
#
#         set_id = driver.find_element_by_name('set_id')  # 选择系列
#         time.sleep(0.1)
#         Select(set_id).select_by_visible_text(commodity_info['所属系列'])
#
#         sku = driver.find_element_by_name('sku')  # 货号
#         sku.clear()
#         sku.send_keys(commodity_info['sku'])
#
#         seller_sku = driver.find_element_by_id("seller_sku")  # 商家sku
#         seller_sku.clear()
#         seller_sku.send_keys(commodity_info['商家货号'])
#
#         tech = driver.find_element_by_name('tech')  # 工艺
#         tech.clear()
#         tech.send_keys(commodity_info['工艺'])
#
#         material = driver.find_element_by_name('material')  # 材质
#         material.clear()
#         material.send_keys(commodity_info['材质'])
#
#         volume = driver.find_element_by_name('volume')  # 体积
#         volume.clear()
#         volume.send_keys('长: %scm  宽: %scm  高: %scm' % (
#             commodity_info['商品长宽高'][0], commodity_info['商品长宽高'][2], commodity_info['商品长宽高'][1]))
#
#         style = driver.find_element_by_name('style')  # 风格
#         style.clear()
#         style.send_keys(commodity_info['风格'])
#
#         price = driver.find_element_by_name('price')  # 价格
#         price.clear()
#         price.send_keys(commodity_info['价格'])
#
#         md5 = driver.find_element_by_name('md5')  # MD5
#         md5.clear()
#         md5.send_keys(commodity_info['规格']['finally']['MD5码'])
#
#         up_image_button = driver.find_element_by_xpath('//*[@id="image"]/div[2]/label')  # 图片上传按钮
#         up_image_button.click()
#         upfile(commodity_info['商品图片地址'].replace('//', '\\'))
#
#         skin_file = driver.find_element_by_name('skin_file')  # 皮肤包文件
#         skin_file.send_keys(commodity_info['规格']['finally']['材质包地址'])
#
#         skin_file_button = driver.find_element_by_css_selector(
#             '#form-add-edit > div:nth-child(17) > div.formControls.col-5 > input:nth-child(7)')  # 上传皮肤包按钮
#
#         skin_file_button.click()
#         colseAlert()
#
#         self.up_option(commodity_info, revise)
#
#         status1 = driver.find_element_by_xpath('//*[@id="form-add-edit"]/div[20]/div[1]/div[1]/label')  # 上架
#         status0 = driver.find_element_by_xpath('//*[@id="form-add-edit"]/div[20]/div[1]/div[2]/label')  # 下架
#
#         position = driver.find_element_by_id('position')  # 排序
#         position.clear()
#         position.send_keys(commodity_info['排序'])
#
#         submit = driver.find_element_by_css_selector('#form-add-edit > div:nth-child(22) > div > input')  # 提交
#         submit.click()
#         time.sleep(4)
#
#     def up_option(self, commodity_info, revise):
#         add = driver.find_element_by_name('add')  # 添加规格
#         if revise is False:
#             i = 0
#             for name, info in commodity_info['规格']['finally']['模型'].items():
#                 add.click()
#
#                 option_name = driver.find_elements_by_id('option_name')[i]  # 规格名称
#                 option_name.clear()
#                 option_name.send_keys(name)
#
#                 option_price = driver.find_elements_by_id('option_price')[i]  # 规格价格
#                 option_price.clear()
#                 option_price.send_keys(info['价格'])
#
#                 option_sku = driver.find_elements_by_id('option_sku')[i]  # 规格sku
#                 option_sku.clear()
#                 option_sku.send_keys(info['sku'])
#
#                 option_image_button = driver.find_element_by_xpath(
#                     '//*[@id="form-add-edit"]/div[18]/div[1]/table/tbody/tr[%s]/td[6]/span/div[2]/label' % (
#                             2 + i))  # 图片上传按钮
#                 # up_image.append(option_image_button)
#                 option_image_button.click()
#                 upfile(info['渲染图片地址'].replace('//', '\\'))
#                 # time.sleep(0.5)
#                 option_model_file = driver.find_elements_by_name('option_model_file')[i]  # 规格模型文件
#                 option_model_file.send_keys(info['模型包地址'])
#                 option_model_file_button = driver.find_element_by_xpath(
#                     '//*[@id="form-add-edit"]/div[18]/div[1]/table/tbody/tr[%s]/td[5]/input[3]' % (2 + i))  # 规格模型上传按钮
#                 option_model_file_button.click()
#                 colseAlert()
#                 # up_file.append(option_model_file_button)
#                 i += 1
#         else:
#             option = driver.find_elements_by_xpath('//*[@name="tables"]/tbody/tr')
#             if len(option[1:]) == len(commodity_info['规格']['finally']['模型'].keys()):
#                 i = 0
#                 for name, info in commodity_info['规格']['finally']['模型'].items():
#                     option_name = driver.find_elements_by_id('option_name')[i]  # 规格名称
#                     option_name.clear()
#                     option_name.send_keys(name)
#
#                     option_price = driver.find_elements_by_id('option_price')[i]  # 规格价格
#                     option_price.clear()
#                     option_price.send_keys(info['价格'])
#
#                     option_sku = driver.find_elements_by_id('option_sku')[i]  # 规格sku
#                     option_sku.clear()
#                     option_sku.send_keys(info['sku'])
#
#                     option_image_button = driver.find_element_by_xpath(
#                         '//*[@id="form-add-edit"]/div[18]/div[1]/table/tbody/tr[%s]/td[6]/span/div[2]/label' % (
#                                 2 + i))  # 图片上传按钮
#                     # up_image.append(option_image_button)
#                     option_image_button.click()
#                     upfile(info['渲染图片地址'].replace('//', '\\'))
#                     # time.sleep(0.5)
#                     option_model_file = driver.find_elements_by_name('option_model_file')[i]  # 规格模型文件
#                     option_model_file.send_keys(info['模型包地址'])
#                     option_model_file_button = driver.find_element_by_xpath(
#                         '//*[@id="form-add-edit"]/div[18]/div[1]/table/tbody/tr[%s]/td[5]/input[3]' % (
#                                 2 + i))  # 规格模型上传按钮
#                     option_model_file_button.click()
#                     colseAlert()
#                     # up_file.append(option_model_file_button)
#                     i += 1
#
#             elif len(option[1:]) < len(commodity_info['规格']['finally']['模型'].keys()):
#                 add.click()
#                 self.up_option(commodity_info, revise)
#
#             else:
#                 driver.find_element_by_xpath('//*[@name="tables"]/tbody/tr[%s]/td[7]' % len(option)).click()
#                 colseAlert()
#                 self.up_option(commodity_info, revise)
#
#
# # 方法主入口
# if __name__ == '__main__':
#     start = time.time()
#     # 加启动配置
#     driver = openChrome()
#     it = InTimeWebUpload()
#     it.login()
#
#     # for i in findSpecifiedFile(r'D:\test','json'):
#     #
#     #     it.add_commodity(i)
#
#     it.add_commodity(findSpecifiedFile(r'D:\test', 'json')[2])
#
#     end = time.time()
#     print(changeTime(end - start))
#     # modification(driver)
#
#     # print(commodity_info['finally']['渲染图片地址'].replace('//','\\'))
