# encoding=utf-8

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import win32gui
import win32con
from pymouse import PyMouse
from pykeyboard import PyKeyboard
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
    userName = driver.find_element_by_name("user")
    userName.send_keys("yingtai")
    pwdName = driver.find_element_by_name("pwd")
    pwdName.send_keys('YT56894!@#')
    a = driver.find_elements_by_class_name('btn')
    a[0].click()
    b = driver.find_elements_by_xpath('//*[@id="menu-article"]/dt/i[2]')
    b[1].click()
    c = driver.find_elements_by_xpath('//*[@id="menu-article"]/dd/ul/li[1]/a')
    c[1].click()
    driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[1])
    d = driver.find_element_by_css_selector(
        'body > div > div:nth-child(3) > table > tbody > tr:nth-child(1) > td.td-manage > a:nth-child(1)')
    d.click()
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    # seller_sku = driver.find_element_by_id("seller_sku")
    # seller_sku.send_keys('王大锤')
    f = driver.find_elements_by_tag_name('label')

    # for i in f:
    #     print(f.index(i), i.get_attribute('style'))

    f[18].click()
    time.sleep(0.5)

    kk = PyKeyboard()
    time.sleep(0.5)

    kk.type_string(r"C:\Users\Intime\Desktop\125017292872085595.png")

    time.sleep(0.5)

    kk.tap_key(kk.enter_key)
    print('aaaa')
    # f[12].send_keys(r"F:\ARKit15 - 副本\AssetBundles\mr01")
    # f[13].click()
    # result = EC.alert_is_present()(driver)
    # while result is False:
    #     time.sleep(1)
    #     result = EC.alert_is_present()(driver)

    # result.accept()

    # f[1].send_keys(r"C:\Users\Intime\Desktop\125017292872085595.png")
    # e = driver.find_element_by_css_selector('#form-add-edit > div:nth-child(22) > div > input')
    # e.click()

    # 提交表单
    # driver.find_element_by_xpath("//*[@id='su']").click()
    # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    # print(a)


# 方法主入口
if __name__ == '__main__':
    # 加启动配置
    driver = openChrome()
    operationAuth(driver)
